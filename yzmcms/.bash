/home/lirongyao0916/Projects/lryper.com
sudo chown -R $USER:www-data /home/lirongyao0916/Projects
sudo chmod -R 2755 /home/lirongyao0916/Projects/lryper.com
sudo find /home/lirongyao0916/Projects/lryper.com -type f -exec chmod 2755 {} \;
ls -ld /home/ /home/$USER /home/$USER/Projects /home/$USER/Projects/lryper.com



#### home 目录添加网站


# 创建网站目录
WEBSITE_DIR="/home/lirongyao0916/Projects/test.com"

# 将目录所有权设为当前用户
sudo chown -R $USER:$USER "$WEBSITE_DIR"

# 设置目录权限为 755（所有者可读写执行，其他用户可读执行）
find "$WEBSITE_DIR" -type d -exec chmod 755 {} \;

# 设置文件权限为 644（所有者可读写，其他用户可读）
find "$WEBSITE_DIR" -type f -exec chmod 644 {} \;

# 验证权限
ls -ld "$WEBSITE_DIR" && ls -l "$WEBSITE_DIR"




# 将 Nginx 用户（www-data）添加到当前用户组
sudo usermod -aG $USER www-data

# 将网站目录的组所有权改为 www-data
sudo chown -R $USER:www-data "$WEBSITE_DIR"

# 设置目录权限为 750（所有者可读写执行，组用户可读执行）
sudo chmod -R 750 "$WEBSITE_DIR"

# 重新加载用户组（使组更改生效）
newgrp www-data

# 验证 www-data 用户是否有权访问
sudo -u www-data ls -l "$WEBSITE_DIR"