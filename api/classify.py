import tensorflow as tf
import numpy as np

def predict(img):  # model and image as input

    model = tf.keras.models.load_model('./model/build')  # model 경로 로드하기

    img_array = tf.keras.preprocessing.image.img_to_array(np.array(img))
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    top_k_values, top_k_indices = tf.math.top_k(predictions, k=5)

    predicted_class = [top_k_indices.numpy()[0][j] for j in range(5)]  #class_names < 레이블 이름이 담긴 배열

    return predicted_class  # 다섯개 확률 높은 결과값 뽑기 순서대로
