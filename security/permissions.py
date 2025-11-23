from .jwt_tokens import *
from ..model import UserRoleEnum, UserProfile


class RoleChecker:

	def __init__(self, allowed_roles):
		self.allowed_roles = allowed_roles

	def __call__(self, user:Annotated[UserProfile, Depends(get_current_active_user)]):
		if user.role in self.allowed_roles:
			return user
		
		raise HTTPException( 
			status_code=status.HTTP_401_UNAUTHORIZED,   
      detail="You don't have enough permissions" 
		) 





admin_required=RoleChecker([UserRoleEnum.admin])
investor_required=RoleChecker([UserRoleEnum.investor])
business_required=RoleChecker([UserRoleEnum.business])
guest_required=RoleChecker([UserRoleEnum.guest])
founder_required=RoleChecker([UserRoleEnum.founder])
institution_required=RoleChecker([UserRoleEnum.institution])





# async def define_role(current_user,  role: UserRoleEnum, user_dependency):

#     if current_user.role == "founder":
#         return {
#             id: ["id"],
#             "message": 'A founder can list his business and require funding',
#             role: ["user.role"]
#         }

#     if current_user.role == "investor" or current_user.role == "institution":
#         return {
#             id: ["id"],
#             "message": 'An investor or institution can see where they have invested and how much, and get some basic info on the startup/ business they have invested on ',
#             role: ["user.role"]
#         }

#     if current_user.role == "guest":
#         return {
#             id: ["id"],
#             "message": 'A guest can only see how the page works',
#             role: ["user.role"]
#         }

#     if current_user.role == "business":
#         return {
#             id: ["id"],
#             "message": 'A founder can check which person has invested in their startup, how much they have invested and how much money they still need to raise',
#             role: ["user.role"]
#         }
    

#     if current_user.role == "admin":
#         return {
#             id: ["id"],
#             "message" : 'An admin can see all users, delete users, edit users, create new users',
#             role: ["user.role"]
#         }

        