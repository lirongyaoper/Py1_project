/home/lirongyao0916/Projects/lryper.com
sudo chown -R $USER:www-data /home/lirongyao0916/Projects
sudo chmod -R 2755 /home/lirongyao0916/Projects/lryper.com
sudo find /home/lirongyao0916/Projects/lryper.com -type f -exec chmod 2755 {} \;
ls -ld /home/ /home/$USER /home/$USER/Projects /home/$USER/Projects/lryper.com