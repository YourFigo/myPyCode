# Copyright 2018 Figo Individual. All Rights Reserved.
# 创建一个模拟滚动条滚动到页面底部函数
def scroll(driv):
    driv.execute_script("""   
    (function () {   
        var y = document.body.scrollTop;   
        var step = 100;   
        window.scroll(0, y);   


        function f() {   
            if (y < document.body.scrollHeight) {   
                y += step;   
                window.scroll(0, y);   
                setTimeout(f, 50);   
            }  
            else {   
                window.scroll(0, y);   
                document.title += "scroll-done";   
            }   
        }   


        setTimeout(f, 1000);   
    })();   
    """)