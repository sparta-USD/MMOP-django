from rest_framework import status, permissions
from rest_framework.exceptions import APIException
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model


# 비로그인 인증 실패시 사용
class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)

class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        # 비로그인 유저
        if not request.user.is_authenticated:
        	# 보낼 메세지
            response ={
                "detail": "로그인한 유저만 접근 가능합니다! 로그인해주세요 ",
            }
            # raise로 에러를 발생시키고 앞서 만들어둔 클래스를 호출, 메세지를 보낸다
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        return bool(request.user and request.user.is_authenticated)


class IsOwnerIsAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    # 목록조회는 모두 허용 / 인증된 유저에만 등록 허용
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # 비로그인 유저
        if not request.user.is_authenticated:
        	# 보낼 메세지
            response ={
                "detail": "로그인한 유저만 접근 가능합니다! 로그인해주세요 ",
            }
            # raise로 에러를 발생시키고 앞서 만들어둔 클래스를 호출, 메세지를 보낸다
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 ​​허용, SAFE_METHODS(GET, HEAD, OPTIONS)요청을 허용 할 것입니다.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 비로그인 유저
        if not request.user.is_authenticated:
        	# 보낼 메세지
            response ={
                "detail": "로그인한 유저만 접근 가능합니다! 로그인해주세요 ",
            }
            # raise로 에러를 발생시키고 앞서 만들어둔 클래스를 호출, 메세지를 보낸다
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        # 인스턴스에는`owner`라는 속성거나 staff이어야합니다.
        return bool((obj.user == request.user) or request.user.is_staff)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
        Object-level permission to only allow admin of an object to edit it.
        Assumes the model user has an `is_staff` attribute.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # 비로그인 유저
        if not request.user.is_authenticated:
        	# 보낼 메세지
            response ={
                "detail": "로그인한 유저만 접근 가능합니다! 로그인해주세요 ",
            }
            # raise로 에러를 발생시키고 앞서 만들어둔 클래스를 호출, 메세지를 보낸다
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        # 비어드민 유저    
        elif not request.user.is_staff:
        	# 보낼 메세지
            response ={
                "detail": "접근 권한이 없습니다.",
            }
            # raise로 에러를 발생시키고 앞서 만들어둔 클래스를 호출, 메세지를 보낸다
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        # 유저는 `is_staff`라는 속성이 있어야합니다.
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 ​​허용되며,
        # 그래서 GET, HEAD, OPTIONS 요청을 허용 할 것입니다.
        if request.method in permissions.SAFE_METHODS:
            return True
        # 비로그인 유저
        if not request.user.is_authenticated:
        	# 보낼 메세지
            response ={
                "detail": "로그인한 유저만 접근 가능합니다! 로그인해주세요 ",
            }
            # raise로 에러를 발생시키고 앞서 만들어둔 클래스를 호출, 메세지를 보낸다
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        # 비어드민 유저    
        elif not request.user.is_staff:
        	# 보낼 메세지
            response ={
                "detail": "접근 권한이 없습니다.",
            }
            # raise로 에러를 발생시키고 앞서 만들어둔 클래스를 호출, 메세지를 보낸다
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        # 유저는 `is_staff`라는 속성이 있어야합니다.
        return bool(request.user and request.user.is_staff)
