


from datetime import date, timedelta
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from typing import IO
from fastapi import APIRouter
import filetype



app = FastAPI()

router = APIRouter(
    prefix= "/investment_validation",
    responses={404: {"description": "Not found"}}
)



#calculate investor age
# def calculate_age(date_of_birth : date) -> int:
#     today = date.today()
#     return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


# #calculate document expiry
# def check_document_expiry(expiry_date: date) -> bool:
#     today = date.today()
#     return expiry_date > today + timedelta(days=90)


# #Sufficient Available Capital 
# 					# 1- investitori duhet te kete minimalisht shumen qe do te investoje
#           # 2 - investitorit i shkon nje reminding mesazh ne rast se ai ben investim qe i merr me shume se 80% te amount qe ka ne llogari
#           # 3- Explicit Consent to Investment Terms


# #capital_available : float
# #amount_investing: float


# # def sufficient_available_capital(capital_available : float , amount_investing: float):
# #     capital_available = 
  
    





# @router.post("/")
# def validate_document(file : IO, date_of_birth : date): # nuk kam bere declare file si basemodel
#     file_size = 2097152

#     accepted_file_types = [
#     "image/jpeg", 
#     "image/png", 
#     "application/pdf", 
#     "application/msword",
#     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]


#     file_info = file.guess(file.file) # kontrollon nese provided file is valid or not
#     if file_info is None: # nese nuk eshte ben raise nje error
#         raise HTTPException(
#             status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#             detail="Unable to determine file type"
#         )
#     detected_content_type = file_info.extension.lower()


#     if ( # kontrolllon nese file provided eshte pjese e file qe jane accepted
#         file.content_type not in accepted_file_types
#         or detected_content_type not in accepted_file_types
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#             detail="Unsupported file type",
#         )
    
#     real_file_size = 0
#     for chunk in file.file:
#         real_file_size += len(chunk)
#         if real_file_size > file_size:
#             raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too large")
        

#     age = calculate_age(date_of_birth)
#     if age < 18:
#         raise HTTPException(status_code=400, detail="User must be 18+ to invest.")
    

#     expiry = check_document_expiry(expiry_date)
#     if (expiry - today) <= timedelta(days=90):
#         raise HTTPException(status_code=400, detail="Document expires in 3 months or less.")
    
    


















































# @app.post("/file")
# def upload_file(file: UploadFile):
#     validate_file_size_type(file)


#     return {"filename" : document.name,
#             "content_type": document.content_type}


		



# @router.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename" : file.name}



# @router.post("/")
# async def upload_and_validate_file(file : UploadFile):
    










# for investment in investments:

# 	if (investor.age >= 18) {
# 		return 
# 	}