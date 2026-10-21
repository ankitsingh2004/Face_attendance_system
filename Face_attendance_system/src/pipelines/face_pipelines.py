# import dlib
# import numpy as np
# import face_recognition_models
# from sklearn.svm import SVC  # Classifies whose face is present
# import streamlit as st

# from src.database.db import get_all_students

# @st.cache_resource
# def load_dlib_models():
#     detector = dlib.get_frontal_face_detector()



#     sp = dlib.shape_predictor(
#         face_recognition_models.pose_predictor_model_location()

#     )

#     facerec =  dlib.face_recognition_models_v1(
#         face_recognition_models.face_recognition_model_location()
#     )


#     return detector, sp, facerec

# #  convert images into arrays of numbers and kind of vector  or you can say convert image into binary forms 
# def get_face_embeddings(image_np):
#     detector, sp, facerec =  load_dlib_models()
#     faces = detector(image_np,1)

#     encodings = []

#     for face in faces:
#         shape = sp(image_np,face)
#         # It will give 68 landmarks 
#         face_descriptor = facerec.compute_face_descriptor(image_np,shape,1)  #128Dimension 

#         encodings.append(np.array[face_descriptor])
#     return encodings


# # Heavy function  don't want rerun again and again 
# @st.cache_resource
# # SVC = It will tell In the photo person is visible and if visible then where that person is visible 
# def get_trained_models():
#     X = []
#     Y = []

#     student_db = get_all_students()

#     if not student_db:
#         return None
#     for student in student_db:
#         embedding = student.get('face_embedding')
#         if embedding:
#             X.append(np.array(embedding))
#             Y.append(student.get('student_id'))
#         if len(X)== 0:
#             return 0

# # straight line we will use here kernel 
# # class_weight it will balance the Photo and it bring the photo in the scale if a person has 100 ,10000 photo it will bring them in the scale and all the photo is same person 
#         clf = SVC(kernel='linear',probability=True,class_weight='blanced')

#         try:
#             clf.fit(X,Y)
#         except ValueError:
#             pass

#         return {'clf':clf,"X":x, "Y":y}




# # when new student will enter then it is used for that 
# def train_classifier():
#     st.cache_resource.clear()
#     model_data= get_trained_models()
#     return bool(model_data)

# def predict_attendance(class_image_np):
#     encodings = get_face_embeddings(class_image_np)

#     detected_student = {} 

#     model_data= get_trained_models()

#     if not model_data:
#         # {} is used for the what is the  value of the embeddings 
#         # [] is used for list of student
#         #  0 is used for  number of student and
#         # return {}, [],0 or we can write it another way 
#         return detected_student,[],len(encodings)

#     clf = model_data['clf']
#     # here we will do prediction 
#     X_train= model_data['X']
#     y_train= model_data['Y']

# # for security and unique value means only student will come one time 
#     all_students = sorted(list(set(y_train)))  # here we get all students 

#     for encoding in encodings:
#         if len(all_students)>=2:
#             predicted_id = int(clf.predict([encodings](0)))
#         else :
#             predicted_id = int(all_students[0])

#         student_embeddings = X_train[y_train.index(predicted_id)]

# # bast_match score =  if both matches or best matches then we will check using mathematically (so that the person is best matches or not this will check =linalg )


#         best_match_score = np.linalg.norm(student_embeddings-encoding)
#         resemblance_threshold = 0.6

#         if best_match_score <= resemblance_threshold:
#             detected_student[predicted_id] = True

#     return detected_student,all_students,len(encoding)



# # ALL MACHINE LEARNING WE COVER HERE 
    




import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


# Convert faces into 128-dimensional numerical embeddings
def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)

    encodings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(
            image_np, shape, 1
        )

        encodings.append(np.array(face_descriptor))

    return encodings


# Train the student face classifier
@st.cache_resource
def get_trained_models():
    X = []
    Y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get("face_embedding")

        if embedding is not None:
            embedding = np.asarray(embedding, dtype=float)

            if embedding.shape == (128,):
                X.append(embedding)
                Y.append(student.get("student_id"))

    if len(X) == 0 or len(set(Y)) < 2:
        return None

    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    try:
        clf.fit(X, Y)
    except ValueError:
        return None

    return {
        "clf": clf,
        "X": X,
        "Y": Y
    }


# Call when a new student's face embedding is added
def train_classifier():
    get_trained_models.clear()
    model_data = get_trained_models()
    return bool(model_data)


def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected_student = {}

    model_data = get_trained_models()

    if not model_data:
        return detected_student, [], len(encodings)

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["Y"]

    all_students = sorted(set(y_train))

    for encoding in encodings:
        if len(all_students) < 2:
            continue

        predicted_id = clf.predict([encoding])[0]

        # Find training embeddings belonging to the predicted student
        student_embeddings = [
            X_train[i]
            for i, student_id in enumerate(y_train)
            if student_id == predicted_id
        ]

        if not student_embeddings:
            continue

        # Compare the detected face with the closest stored embedding
        best_match_score = min(
            np.linalg.norm(embedding - encoding)
            for embedding in student_embeddings
        )

        resemblance_threshold = 0.6

        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True

    return detected_student, all_students, len(encodings)
