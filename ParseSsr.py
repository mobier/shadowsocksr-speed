import base64

def fill_padding(base64_encode_str):
   need_padding = len(base64_encode_str) % 4 != 0
   if need_padding:
       missing_padding = 4 - need_padding
       base64_encode_str += '=' * missing_padding
   return base64_encode_str

def base64_decode(base64_encode_str):
   base64_encode_str = fill_padding(base64_encode_str)
   return base64.urlsafe_b64decode(base64_encode_str).decode('utf-8')
def parse(base64_encode_str): #
   decode_str = base64_decode(base64_encode_str)
   parts = decode_str.split(':')
   if len(parts) != 6:
       print('不能解析SSR链接: %s' % base64_encode_str)
       return
   if parts[1]=="443" or parts[1]=="444":
      return parse_ssr(base64_encode_str)
   else:
      return parse_ssr(base64_encode_str)
def parse_ssr_433(base64_encode_str):
   decode_str = base64_decode(base64_encode_str)
   #print(decode_str)
   parts = decode_str.split(':')
   if len(parts) != 6:
       print('不能解析SSR链接: %s' % base64_encode_str)
       return
   server = parts[0]
   port = parts[1]
   protocol = parts[2]
   method = parts[3]
   obfs = parts[4]

   password_and_params = parts[5]
   password_and_params = password_and_params.split("/?")
   params = password_and_params[1]

   param_parts = params.split('&')
   password_encode_str = param_parts[1]
   password_encode_str=password_encode_str.split('=')[1]
   password = base64_decode(password_encode_str)
   port=password.split(':')[0]
   password=password.split(':')[1]

   param_dic = {}
   for part in param_parts:
       key_and_value = part.split('=')
       param_dic[key_and_value[0]] = key_and_value[1]

   obfsparam = base64_decode(param_dic['obfsparam'])
   protoparam = base64_decode(param_dic['protoparam'])
   remarks = base64_decode(param_dic['remarks'])
   group = base64_decode(param_dic['group'])

   ss_result={}
   ss_result['server']=server
   ss_result['port']=port
   ss_result['protocol']=protocol
   ss_result['method']=method
   ss_result['password']=password
   ss_result['obfs']=obfs
   ss_result['obfsparam']=obfsparam
   ss_result['remarks']=remarks
   ss_result['group']=group
   ss_result['protoparam']=protoparam

   # print('server: %s, port: %s, 协议: %s, 加密方法: %s, 密码: %s, 混淆: %s, 混淆参数: %s,  备注: %s, 分组: %s'
   #       % (server, port, protocol, method, password, obfs, obfsparam, remarks, group))
   #print(ss_result)
   return ss_result


def parse_ssr(base64_encode_str):
   decode_str = base64_decode(base64_encode_str)
   parts = decode_str.split(':')
   if len(parts) != 6:
       print('不能解析SSR链接: %s' % base64_encode_str)
       return

   server = parts[0]
   port = parts[1]
   protocol = parts[2]
   method = parts[3]
   obfs = parts[4]
   password_and_params = parts[5]
   password_and_params = password_and_params.split("/?")
   password_encode_str = password_and_params[0]
   password = base64_decode(password_encode_str)
   params = password_and_params[1]
   param_parts = params.split('&')

   param_dic = {}
   ss_result={}
   for part in param_parts:
       key_and_value = part.split('=')
       param_dic[key_and_value[0]] = key_and_value[1]

   obfsparam = base64_decode(param_dic['obfsparam'])
   if('protoparam' in param_dic):
      protoparam = base64_decode(param_dic['protoparam'])
      ss_result['protoparam']=protoparam
   remarks = base64_decode(param_dic['remarks'])
   group = base64_decode(param_dic['group'])

   ss_result['server']=server
   ss_result['port']=port
   ss_result['protocol']=protocol
   ss_result['method']=method
   ss_result['password']=password
   ss_result['obfs']=obfs
   ss_result['obfsparam']=obfsparam
   ss_result['remarks']=remarks
   ss_result['group']=group


   return ss_result
   # print("解析结果:")
   # print('server: %s, port: %s, 协议: %s, 加密方法: %s, 密码: %s, 混淆: %s, 混淆参数: %s, 协议参数: %s, 备注: %s, 分组: %s'
   #       % (server, port, protocol, method, password, obfs, obfsparam, protoparam, remarks, group))

 #python /home/nu11/.config/electron-ssr/shadowsocksr/shadowsocks/local.py -s hk2.pyjiaoyi.cf -p 10384 -k EoWjVthG -m chacha20-ietf -O auth_aes128_md5 -o http_simple -g download.windowsupdate.com -b 0.0.0.0 -l 1080
 #python3 shadowsocksr/shadowsocks/local.py -s us1.pyjiaoyi.cf -p 10384 -k EoWjVthG -m chacha20-ietf -O auth_aes128_md5 -o http_simple -g download.windowsupdate.com -b 0.0.0.0 -l 6666
#s hk2.pyjiaoyi.cf -p 10384 -k EoWjVthG -m chacha20-ietf -O auth_aes128_md5 -o http_simple -g download.windowsupdate.com -b 0.0.0.0 -l 1080
