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

            # 1. 筛选地区为美国的节点（不限定端口）
            if "美国" in line or "US" in line:
                # 动态正则提取标准的 IP 和 真实端口 (例如 107.172.137.69:8443)
                match = re.search(r'\b((?:[0-9]{1,3}\.){3}[0-9]{1,3}):([0-9]{2,5})\b', line)
                if match:
                    ip = match.group(1)
                    port = match.group(2)
                    ip_port = f"{ip}:{port}"
                    
                    # 按原始顺序去重
                    if ip_port not in candidates:
                        candidates.append(ip_port)

        # 2. 直接按原始质量排序截取前 25 个美国节点
        selected_items = candidates[:25]

        print(f"🔍 成功获取并截取排名前 {len(selected_items)} 个美国节点（任意端口）！")

        # 3. 格式化并追加序列号 (#美国01 ~ #美国25)
        us_proxies = []
        for count, item in enumerate(selected_items, start=1):
            formatted_line = f"{item}#美国{count:02d}"
            us_proxies.append(formatted_line)

        # 4. 写入 us_proxies.txt
        with open("us_proxies.txt", "w", encoding="utf-8") as f:
            for proxy in us_proxies:
                f.write(proxy + "\n")

        print(f"✅ 成功写入排名前 {len(us_proxies)} 个美国节点！")

    except Exception as e:
        print(f"❌ 抓取失败: {e}")

if __name__ == "__main__":
    update_proxies()
