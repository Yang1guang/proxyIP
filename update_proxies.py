import requests
import re

def update_proxies():
    url = "https://proxyip.chatkg.qzz.io/alive.txt"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        lines = response.text.splitlines()

        candidates = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 1. 筛选包含 443 端口（排除 8443 干扰）且地区为美国的 IP 节点
            if (":443" in line or ("443" in line and "8443" not in line)) and ("美国" in line or "US" in line):
                # 匹配提取标准 IPv4 地址
                ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
                if ip_match:
                    ip = ip_match.group(0)
                    # 保持原始顺序去重
                    if ip not in candidates:
                        candidates.append(ip)

        # 2. 直接按原始排序顺序截取前 25 个节点
        selected_ips = candidates[:25]

        print(f"🔍 成功获取并截取排名前 {len(selected_ips)} 个美国 443 节点！")

        # 3. 格式化并追加序列号 (#美国01 ~ #美国25)
        us_proxies = []
        for count, ip in enumerate(selected_ips, start=1):
            formatted_line = f"{ip}:443#美国{count:02d}"
            us_proxies.append(formatted_line)

        # 4. 写入 us_proxies.txt
        with open("us_proxies.txt", "w", encoding="utf-8") as f:
            for proxy in us_proxies:
                f.write(proxy + "\n")

        print(f"✅ 成功写入排名前 {len(us_proxies)} 个美国 443 节点！")

    except Exception as e:
        print(f"❌ 抓取失败: {e}")

if __name__ == "__main__":
    update_proxies()
