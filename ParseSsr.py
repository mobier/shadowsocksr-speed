import base64

#python /home/nu11/.config/electron-ssr/shadowsocksr/shadowsocks/local.py -s hk2.pyjiaoyi.cf -p 10384 -k EoWjVthG -m chacha20-ietf -O auth_aes128_md5 -o http_simple -g download.windowsupdate.com -b 0.0.0.0 -l 1080
#python3 shadowsocksr/shadowsocks/local.py -s us1.pyjiaoyi.cf -p 10384 -k EoWjVthG -m chacha20-ietf -O auth_aes128_md5 -o http_simple -g download.windowsupdate.com -b 0.0.0.0 -l 6666
#s hk2.pyjiaoyi.cf -p 10384 -k EoWjVthG -m chacha20-ietf -O auth_aes128_md5 -o http_simple -g download.windowsupdate.com -b 0.0.0.0 -l 1080


def base64_decode(base64_encode_str):
    """ 利用 base64.urlsafe_b64decode 对字符串解码 """
    
    if base64_encode_str:
        need_padding = len(base64_encode_str) % 4
        if need_padding != 0:
            missing_padding = 4 - need_padding
            base64_encode_str += '=' * missing_padding
        return base64.urlsafe_b64decode(base64_encode_str).decode('utf-8')
    return base64_encode_str

def parse(ssrUrl):
    """ 解析ssr链接 
    args: 
        ssrUrl: SSR 链接
    return: 
        ssr_result: SSR链接解析结果
    """

    ssr_result = {}

    decode_str = base64_decode(ssrUrl)
    parts = decode_str.split(':')
    if len(parts) != 6:
        print('不能解析SSR链接: %s' % ssrUrl)
        return
    
    server = parts[0]
    port = parts[1]
    protocol = parts[2]
    method = parts[3]
    obfs = parts[4]

    password_and_params = parts[5]
    password_and_params = password_and_params.split("/?")
    password = base64_decode(password_and_params[0])
    if len(password_and_params) == 1:
        obfsparam = ""
        protoparam = ""
        remarks = ""
        group = ""
    else:
        param_dic = {}
        param_parts = password_and_params[1].split('&')
        for part in param_parts:
            key_and_value = part.split('=')
            param_dic[key_and_value[0]] = key_and_value[1]

        obfsparam = base64_decode(param_dic.get('obfsparam', ""))
        protoparam = base64_decode(param_dic.get('protoparam', ""))
        remarks = base64_decode(param_dic.get('remarks', ""))
        group = base64_decode(param_dic.get('group', ""))
        
    ssr_result['server']=server
    ssr_result['port']=port
    ssr_result['protocol']=protocol
    ssr_result['method']=method
    ssr_result['password']=password
    ssr_result['obfs']=obfs
    ssr_result['obfsparam']=obfsparam
    ssr_result['remarks']=remarks
    ssr_result['group']=group
    ssr_result['protoparam']=protoparam

    return ssr_result


if __name__ == "__main__":
    test_ssrUrl_list = [
        "ssr://MTQyLjkzLjg0LjE1Mzo4ODgwOmF1dGhfY2hhaW5fYTpub25lOnBsYWluOmJYbGFha0kxYWtoMVpuaFZNRGhLWWxkd1lYTnpkMjl5WkE",

        "ssr://NTAuMy4yNDIuMTMzOjEyNTE0OmF1dGhfc2hhMV92NDpjaGFjaGEyMDpodHRwX3NpbXBsZTpOalUwTnprLz9vYmZzcGFyYW09JnByb3RvcGFyYW09JnJlbWFya3M9Nzd5SU1URXVNVEh2dklubGhZM290TG5tdFl2b3I1WG9pb0xuZ3JrSzZabVE2WUNmTXpBd2EySXZjLW1jZ09pbWdlbXJtT21Bbi1lYWhPaUtndWVDdVZGUk1USXdPREU0TmpreU53Jmdyb3VwPQ",

        "ssr://OTEuMTkyLjgxLjMxOjgwOmF1dGhfY2hhaW5fYTpub25lOmh0dHBfc2ltcGxlOllXUnRhVzVoWkcxcGJtRmtiV2x1Lz9vYmZzcGFyYW09JnByb3RvcGFyYW09TVRweGNYRjNaR1kmcmVtYXJrcz01TC1FNVp1OSZncm91cD0",

        "ssr://MTY3LjE3OS43NC4zNDoyNzcwMTphdXRoX2NoYWluX2E6bm9uZTpwbGFpbjpPRGs0TkRJNGFHaGtjZy8_b2Jmc3BhcmFtPSZwcm90b3BhcmFtPSZyZW1hcmtzPTZMU3Q1TG13NVlxZ1VWRTFNVFl3TkRVNEN1LThpT2F0cE9XSWh1UzZxLW1aa09tQW4tLThpUSZncm91cD0",

        "ssr://MTc2LjMyLjM1LjI1NDoyNTAzMTphdXRoX2NoYWluX2E6YWVzLTI1Ni1jZmI6cGxhaW46TmpVME16SXgvP29iZnNwYXJhbT0mcHJvdG9wYXJhbT0mcmVtYXJrcz1NVGMyTGpNeUxqTTFMakkxTkEmZ3JvdXA9",

        "ssr://MTM5LjE4MC4yMTMuMjE6MTY0Mjc6b3JpZ2luOmFlcy0yNTYtY2ZiOnBsYWluOk1XTlZSR1kxLz9vYmZzcGFyYW09JnByb3RvcGFyYW09JnJlbWFya3M9YUhWcExXcHBMbmg1ZXVhenFPV0dqT21BZ1RFd1ItYTFnZW1Iai1hV3NPV0tvT1dkb1EmZ3JvdXA9NTRHdzVweTY",

        "ssr://MTc2LjMyLjM1LjI1NDoyNTAzMTpvcmlnaW46YWVzLTI1Ni1jZmI6cGxhaW46TmpVME16SXg"
    ]
    print("解析结果:\n*===========================*")
    for url in test_ssrUrl_list:
        ssr = parse(url[6:])
        print(' server: %s\n port: %s\n 协议: %s\n 加密方法: %s\n 密码: %s\n 混淆: %s\n 混淆参数: %s\n 协议参数: %s\n 备注: %s\n 分组: %s'
          % (ssr["server"], ssr["port"], ssr["protocol"], ssr["method"], ssr["password"], ssr["obfs"], ssr["obfsparam"], ssr["protoparam"], ssr["remarks"], ssr["group"]))
        print("*===========================*")
