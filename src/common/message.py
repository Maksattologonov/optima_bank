raw = """
<!DOCTYPE html>
<html>
<header> 
    <style type="text/css">
        div {
            padding: 10px;
            margin: auto;
            text-align: center;
            border-radius: 10px;
       }
        @media screen and (max-device-width: 1600px) {
        #inDiv {width: 450px;}
        #outDiv {width: 500px;}
        h3 {font-size: 24px;}
        h1 {font-size: 30px;}
        p {font-size: 15px;}
        img {width: 210px}
       }
       @media screen and (max-device-width: 800px) {
        #inDiv {width: 200px;}
        #outDiv {width: 250px;}
        h3 {font-size: 14px;}
        h1 {font-size: 15px;}
        p {font-size: 9px;}
        img {width: 150px}
        }
    </style>
</header>
<body style="margin: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
<div id="outDiv" style="background: #efefef;">
    <div id="inDiv" style="background: white;">
        <img src="https://cards.optimabank.kg/images/design/logo.png" alt="альтернативный текст">
        <h1 style="background-color: rgba(226, 0, 26, 1); padding: 10px 10px; border-radius: 5px; color: white;">
        Подтвердите Ваш электронный адрес</h1>
        <h3 style="margin-bottom: 100px;">Здравствуйте <b style="text-transform: uppercase;">
        {{ messages.name }}</b>!</h3>
        <h3 style="margin-bottom: 20px;">Проверочный код:</h3>
        <h1 style="margin-bottom: 20px">{{ messages.code }}</h1>
        <p style="margin-bottom: 10px; color: rgba(84, 84, 84, 1);">
            Пожалуйста, никому не пересылайте это сообщение, иначе безопасность Вашего аккаунта окажется под угрозой.
        </p>
        <p style="margin-bottom: 10px; color: rgba(84, 84, 84, 1);">Пользуйтесь с удовольствием! С уважение команда OptimaBank</p>
        
    </div>
</div>
</body>
</html>
"""