from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras import models
from keras.tensorflow import layers
from tensorflow.keras.callbacks import EarlyStopping

### Load pre-trained model weights of VGG16 from keras
def load_model():
    model = VGG16(weights="imagenet", include_top=False, input_shape=(100,50,3))
    return model

### As it is a lot of weights we dont want to re-train them as it would take foreva
def set_non_trainable_layers(model):
    model.trainable=False
    return model

### Adding the flatten layer and the dense layers, this are the weeights we will be training
def add_last_layers(model):
    base_model=set_non_trainable_layers(model)
    flattening_layer=layers.Flatten()
    dense_layer=layers.Dense(64,activation='relu')
    model.add(layers.Dropout(0.15))
    dense_layer=layers.Dense(32,activation='relu')
    prediction_layer=layers.Dense(1,activation='sigmoid')

    model=models.Sequential([
                            base_model,
                            flatten__layer,
                            dense_layer_1,
                            dense_layer_2,
                            prediction_layer
                            ])
    return model

### Add the compiler
def compile_model(model):

    opt = optimizers.Adam(learning_rate=0.1)
    model.compile(loss='binary_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    return model

###Actually building the model now using the functions above
def build_model():

    model = load_model()
    model = add_last_layers(model)
    model = compile_model(model)

    return model

#model = build_model() ## uncomment if you want to build the model

### Fitting the model
def fit_model(model,X_train,y_train)
    es=EarlyStopping(patience=7,restore_best_weights=True)

    history=model.fit(X_train,y_train,validation_split=0.2,batch_size=16,
                    epochs=600,callbacks=[es],verbose=1)
    return history

### First baseline evaluation
def evaluate_model(model,X_test,y_test)
    res=model.evaluate(X_test,y_test,verbose=0)
    return res
