from django.db import models
# AbstractBaseUser: check be unique( tồn tại duy nhất),tạo 1 đối tượng user mới
# AbstractUser: Tạo 1 đối tượng user có các field đã có sẵn của user
# PermissionsMixin: check quyền là admin hay client
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

#  tạo thêm class này vì đã thay thế field username bằng field email do đó tạo ra class này để quản lý
class UserProfileManager(BaseUserManager):
  """Manage for user profile"""

  def create_user(self,email,name,password=None):
    """Create a new user profile"""
    if not email:
      raise ValueError('User must have an email address')
    email = self.normalize_email(email)  # bắt buộc sau dấu @ đều phải là chữ thường
    user = self.model(email=email,name=name)
    # Không truyền password lên trên do phải truyền dưới dạng hàm băm chứ k được lưu dưới dạng văn bản thuần
    user.set_password(password)
    #  Thêm using để có thể dùng nhiều loại db
    user.save(using = self._db)

    return user
  
  def create_superuser(self,email,name,password):
    user = self.create_user(email,name,password)
    user.is_superuser = True
    user.is_staff = True
    user.save(using = self._db)

    return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
  # Mô hình cơ sở dữ liệu cho người dùng trong hệ thống
  email = models.EmailField(max_length=255,unique=True)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserProfileManager()

  # Thay vì cung cấp tên và pass thì cung cấp email và pass để đăng nhập
  USERNAME_FIELD = 'email'
  # field bắt buộc của user
  REQUIRED_FIELDS = ['name']

  def get_full_name(self):
    return self.name

  def __str__(self):
    return self.email
