###
 # @Author: hibana2077 hibana2077@gmail.com
 # @Date: 2024-05-26 15:08:15
 # @LastEditors: hibana2077 hibana2077@gmail.com
 # @LastEditTime: 2024-05-26 15:08:39
 # @FilePath: \grad_project\redeploy.bash
 # @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
### 
git pull

sudo docker compose down

sudo docker compose up -d --build