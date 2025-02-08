
### -- modele 结构-- ####

卡牌：Card（属性类似于一个技能）
	类别： 【行动， 能力，召唤】
	需要行动力： 【1点，2点，3点，。。。。。】
	韧性值：【】
	状态：【未出，半出，全出】
	效果：
	    范围 【】
	    防御增加[x]
		聚类[x]内地人
		造成地人【x】伤害


英雄： Hero
    
	职业：Carrer
	    carrer_id
		carrer_name
		carrer_level      # 职业品阶
		male_mode         # 职业模型男
		female_mode       # 职业模型女
		carrer_icon       # 职业icon
		carrer_max_level  # 职业最高品阶
		carrer_update_exp # 升级经验	


地图：Map
      

战场：BattleField
    
	MapID         # 战局使用的地图
	Players_1     # 玩家1
	Players_2     # 玩家2

	回合：Round



玩家： Player
     
    设备：Device
	     terminalType         # 终端类型
		 model                # 设备型号
		 os_version           # 操作系统版本
		 uuid                 # 设备UUID
		 client_version       # 客户端应用版本
		 mac                  # mac 地址
		 idfa                 # idfa
	
	用户： UserInfo
	    user_name 
		passwd
		email
		phone
		join_time
		last_login_time
		last_logout_time
		faild_login_time
		last_login_ip
		last_login_terminal_type               # 
		last_login_local                       # 地域
		last_login_client_version
		lock_status
		lock_time 
		lock_reason
		today_online_time
		addicted_flag                          # 沉迷标志
		
		 

