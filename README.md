#openwrtgod

##openwrt 编译记录



### 20170330
>   在fstab添加对SDCARD读取的支持,fstab支持热插拔，单靠block不行
>   在自启动脚本中添加SDCARD mount

    package/base-files/files/etc/rc.local
<pre><code>
uci add fstab mount
uci set fstab.@mount[0].enabled=1
uci set fstab.@mount[0].fstype=vfat
uci set fstab.@mount[0].device=/dev/mmcblk0p1
uci set fstab.@mount[0].target=/mnt/eotusd
uci set fstab.@mount[0].options=rw,sync,noatime
uci commit fstab
/etc/init.d/fstab restart

echo "start to run insert sd to mount SD CARD"
/usr/bin/insert_sd.sh &

echo "start to run eotu_wifidog"
/etc/init.d/eotu_wifidog.sh start

ln -s /mnt/eotusd /www/
    
</pre></code>



<<<<<<< HEAD
HTTP/0.0 503 Service Unavailable
Date: Saturday, 18-Feb-17 16:07:09 CST
Keep-Alive: timeout=38

EOF
=======
### 20170218

>   修改/etc/config/network内容：

    /openwrt/package/base-files/files/bin/config_generate.sh
    --添加中继
		delete network.wwan 
		set network.wwan='interface'
		set network.wwan.proto='dhcp'
    --添加SIM卡上网APN拨号上网
		delete network.wan2
		set network.wan2='interface'
		set network.wan2.proto='3g'
		set network.wan2.service='umts'	
		set network.wan2.maxwait='0'
		set network.wan2.device='/dev/ttyUSB2'
		set network.wan2.apn='internet'
		set network.wan2.pincode=''
		set network.wan2.username=''
		set network.wan2.password=''
		
>   修改/etc/config/firewall内容：

    /openwrt/package/network/config/firewall/files/firewall.config
    增加支持端口wan2 和wwan
    config zone
	option name		wan
	list   network		'wan'
	list   network		"wan2"
	list   network		'wan6'
	list   network		'wwan'	
	option input		REJECT
	option output		ACCEPT
	option forward		REJECT
	option masq		1
	option mtu_fix		1

>   修改/etc/wireless内容

    /openwrt/package/kernel/mac80211/files/lib/wifi/mac80211.sh
    --默认打开wifi	option disabled 0   
    	
    config wifi-iface 'stamode'
	option network 'wwan'
	option ssid 'wx-s.netXXXXXt'
	option encryption 'psk2'
	option device 'radio0'
	option mode 'sta'
	option bssid '14:75:90:E2:77:88'
	option key 'XXX'
    config wifi-iface 'apmode'
	option device radio$devidx
	option mode 'ap'
	option encryption 'none'
	option ssid 'Eotu_GS'
	option network 'lan'





# 记录
    
### README

>	eotu_router_plat	服务端程序

>	plat_test		简化的服务端测试程序

>	eotu_wifidog		openwrt wifidog修改源码

>	server_demo		eotu server demo
	
### openwrt SDK 版本

> 官方trunk源：git clone git://git.openwrt.org/packages.git
	MT7620 可以选择的target profile 多，目前选择 GL-MT750

> trunk源2：	git clone https://github.com/openwrt/openwrt.git
	对于MT7620,target profile选择少，目前不适用

> chao 源： 对MT7620支持更少

> breaker--bb 源：  待测

### 20170118

	经测验，路由器唯一网口对应4号端口，VLAN2 为WAN口，VLAN1为LAN口

config switch_vlan                        
        option device 'switch0'           
        option vlan '1'                   
        option ports '1 2 3 4 6t'         
                                          
config switch_vlan                        
        option device 'switch0'           
        option vlan '2'                   
        option ports '0 6t'
>>>>>>> 5d5b221249448f4b3ef436ee4b4607869010a89f
