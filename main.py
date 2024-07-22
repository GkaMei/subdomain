import Plugins.domain.check_url as check_url
import Plugins.domain.crt_sh as crt_sh
import Plugins.domain.ksubdomain as ksubdomain
import Plugins.domain.chaziyu_com as chaziyu_com
import Plugins.domain.dig as dig
import Plugins.ResultToFile.result_to_file as result_to_file
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_domain(domain):
    """
    检查域名是否存在泛解析。
    :return: 如果不存在泛解析，返回True；否则返回False
    """
    result = check_url.random_to_A(domain)
    if result == 5:
        print("该域名存在泛解析")
        return False
    else:
        print("该域名不存在泛解析,开始爆破子域名")
        return True

def get_subdomains(domain):
    """
    并行获取子域名。
    :return: 包含各个服务结果的字典
    """
    with ThreadPoolExecutor() as executor:
        # 提交任务到线程池
        futures = {
            executor.submit(crt_sh.get_subdomains, domain): 'crt_sh',
            executor.submit(chaziyu_com.get_subdomains, domain): 'chaziyu_com',
            executor.submit(dig.get_subdomains, domain): 'dig',
            executor.submit(ksubdomain.execute_command, domain): 'ksubdomain'
        }
        
        results = {}
        # 迭代完成的任务
        for future in as_completed(futures):
            service_name = futures[future]
            try:
                result = future.result()
                results[service_name] = result
            except Exception as e:
                print(f"{service_name} generated an exception: {e}")
        
        return results

def main():
    """
    主函数，获取用户输入的域名并执行子域名获取和保存操作。
    """
    domain = input("请输入域名:")
    if check_domain(domain):
        results = get_subdomains(domain)
        result_to_file.save_result_to_file(results)

if __name__ == '__main__':
    main()