import  math

import  tensorflow          as  tf
import  tensorflow.keras.backend        as  K
from    tensorflow.keras.layers         import  Lambda 


def policy_loss_func(advantage, eps=1.e-16):
    ''' Policy loss function
    '''
    def _neglogp(x, mu, sigma):
        return (
            .5*K.sum(K.square((x - mu) / sigma), axis=-1, keepdims=True)
            + .5*K.sum(K.log(2.*math.pi*K.square(sigma) + eps), axis=-1, keepdims=True)
        )

    def _entropy(sigma):
        return K.sum(K.log(sigma + eps) + .5*math.log(2.*math.pi*math.e), axis=-1, keepdims=True)

    def _loss(y_true, y_pred, alpha=0.01):
        # Parse inputs
        mu, log_sigma = tf.split(y_pred, num_or_size_splits=2, axis=-1)
        sigma = K.exp(log_sigma)
        
        # Get negative logarithmic of Gaussian distribution
        neglogp = K.mean(_neglogp(y_true, mu, K.exp(log_sigma)))
        
        # Eligibility
        eligibility = K.mean(K.stop_gradient(advantage) * neglogp)
        
        # Entropy
        entropy = K.mean(_entropy(K.exp(log_sigma)))

        return eligibility - alpha*entropy

    return _loss


def value_loss_func(y_true, y_pred, beta=.5):
    ''' Value loss function
    '''
    return beta*K.mean(K.square(y_true - y_pred))
