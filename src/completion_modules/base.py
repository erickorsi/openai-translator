from abc import ABC, abstractmethod

class BaseCompletion(ABC):
    '''
    Base class for all completions.
    '''
    @abstractmethod
    def run(self):
        '''
        Base method to run the completion and return the result.
        '''
        return None
