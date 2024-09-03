# from auth import Auth


# def require_auth(path: str, excluded_paths) -> bool:
#     """
#     Returns True if the path requires authentication, False otherwise.
#     """
#     if path is None or not excluded_paths:
#         return True
    
#     normalized_path = path.rstrip('/')
#     normalized_excluded_paths = [p.rstrip('/') for p in excluded_paths]
#     print("normalized_excluded_paths")
#     return normalized_path not in normalized_excluded_paths

# exclude_paths =['/api/v1/status/',
#             '/api/v1/unauthorized/',
#             '/api/v1/forbidden/',
# ]

# print(require_auth(path='/api/v1/status/', excluded_paths ))

       