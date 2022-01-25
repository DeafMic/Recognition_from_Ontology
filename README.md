Performs offline speech recognition with the help of PicoVoice recognizer and Onthologies.

Rhino module from the PicoVoice proved to be the most reliable voice recognizer which was found. Very accurate results can be achieved with monimum tweaking.
Voice models are trained online on the following website: https://console.picovoice.ai/rhn

You would have to create your own account. Each model created has 30 days expiration time, after which the same model can be retrained in the rhino console with the new expiration date. 

While Rhino module handles actual voice recognition, Porcupine is the module which trains the wake words. In this way in order to say the wanted word, the user first needs to say the wake word (i.e. "Alexa"), after which the actual word can be said.
