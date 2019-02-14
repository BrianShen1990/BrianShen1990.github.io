Web Frameworks Sharing / Web框架分享
##########################################


:date: 2018-09-19
:tags: React, Store, Reflux, Web, Node
:category: Web
:slug: Web_Sharing
:author: Brian Shen
:summary: Web Knowledge

.. _web_sharing_rst:

.. contents::


Why we should use UI Frameworks? / 为什么我们要使用框架
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are reasons, but not why we use it. / 这些是理由，但是，其实并不是真正的原因:

    - They are based on components; / 组件基础
    - They have a strong community; / 强大的社区
    - They have plenty of third party libraries to deal with things; /  第三方模块和库
    - They have useful third party components;  / 第三方组件
    - They have browser extensions that help debugging things;  / 浏览器调试更加的方便

The most important thing is that: / 最重要的是:

- Keeping the UI in sync with the state is hard. / 将 UI 保持与状态一致， 是一件非常困难的事情.
    It is not possible to write complex, efficient and easy to maintain UIs with Pure JavaScript.
    如果不引入这些框架， 我们很难写出复杂 高效 和 可维护的App.

- Keep focusing on data handling. / 将更多的精力集中在写有用的代码上。
    
Example
*******

Let's write a simple UI with state.
我们写一个简单的带state 的UI 进行查看。

.. code-block:: bash

    <html>
        <head>
            <script type="text/javascript" src="jquery-3.3.1.min.js"></script>
            <script type="text/javascript" src="test.js"></script>
        </head>
        <body>
            <div>
                <h5>Test</h5>
                <input type="text" id="name" />&nbsp;
                <input type="button" id="butonClick" value="Add" />
                <ul id="names">
                </ul>
            </div>
        </body>
    </html> 

    $(document).ready(function(){
        let names = [];
        let rebindClick = function(){
            $(".deleteBtn").click(function(){
                let item = $(this).attr("data");
                let index = names.indexOf(item);
                if (index > -1) {
                names.splice(index, 1);
                }
                reRender();
            });
            
        };
        let reRender = function(){
            let htmls = "";
            names.map(item=>{
                htmls += item + '&nbsp;<input class="deleteBtn" type="button" data="' + item + '" value="Delete" />'
            });
            $("#names").html(htmls);
            rebindClick();
        };
        $("#butonClick").click(function(){
            let value = $("#name").val();
            names.push(value);
            reRender();
        });
    })

.. figure:: /images/web/web_sharing_0002.png

When :code:`names` updates, ui won't update unless we manually handle it. 
In this situation, we only have one global variable, so it seems we can still handle it. 
But if we have thousands of variables, it will be a diasaster to handle and watch them all.

当全局状态 :code:`names` 更新时， UI 并不会跟着改变，除非我们手动的去处理他。
在这种情况下， 我们只有一个全局变量， 我们跟踪起来已经需要做很多的事情了，如果变量多时， 处理和监听这些变量需要花费很多的精力。

.. code-block:: bash

    import React, { Component } from 'react';

    class SampleState extends Component {
        constructor(props) {
            super(props);
            this.clickAdd = this.clickAdd.bind(this);
            this.clickDelete = this.clickDelete.bind(this);
            this.nameChange = this.nameChange.bind(this);
            this.state = {
                inputValue: "",
                names: []
            };
        }
        nameChange(event){
            this.setState({"inputValue" : event.target.value});
        }
        clickAdd(){
            let names = this.state.names;
            names.push(this.state.inputValue);
            this.setState({"names": names})
        }
        clickDelete(item){
            let names = this.state.names;
            let index = names.indexOf(item);
            if (index > -1) {
                names.splice(index, 1);
            }
            this.setState({
                "names": names,
                "inputValue": ""
            });
        }
        render(){
            return <div>
                <h5>Test</h5>
                <input type="text" value={this.state.inputValue} onChange={this.nameChange}/>&nbsp;
                <input type="button" onClick={this.clickAdd} value="Add" />
                <ul>
                { this.state.names.map(item=>{return <li>
                    {item}&nbsp;<input type="button" onClick={() => { this.clickDelete(item) }} value="Delete" />
                </li>}) }
                </ul>
            </div>;
        }
    }
    export {  SampleState };

Every time we update state, UI will update automatically. We only need to focus on our data.

每一个当我们去更改state的时候， UI 会自动跟着改变。 因此，我们只需要关注数据即可， 数据正确， 渲染，一定也是正确的。UI 一定会保持与数据的一致性。

.. figure:: /images/web/web_sharing_0001.png

For DE
*******

- Easy coding & efficiency / 简化编程， 提高效率
    - Do less, get more. / 写更少的程序，获得更好的效果
    - Understandable code. / 易懂的代码
- Easy Learning for all RD / 学习曲线平滑， 容易入门， RD 可修改
    - Backend developers can also add simple features without problem. / 后端工程师也能够快速的实现自己想要添加的修修改改
    - Frontend developers can do better and do enhancements. / 前端工程师 在优化时 可控
- Scalability & Ecosystem / 扩展性 和 生态系统 
    - Plugins and Modules / 丰富的插件 和 模块，开发者社区
    - Maintainability / 可维护性
- Cost of Upgrading / 升级代价
    - No framework to framework / 从无框架到有框架的扩展
    - Framework self upgrading / 框架本身升级 


As one of Node users, 
I will recommend React because everything is composed of Node, ES6, Object and strict data flow.
It bridges the gap between Node backend and UI.

作为了一个 Node 的使用者，我会毫不犹豫的推荐React， React 的一切都是由 Node ES6 对象 和 严格的数据流构成的。
在前后端基本没有太多的区别， 很多模块都是共用的。

And that is the reason why I recommend React for DE as most of us are backend developers.
We don't want to touch difficult HTML, CSS. But for ES (JS), it looks like Python and any other languages. 

这也是我为什么会去推荐 DE 团队 以及 整个亚信安全 这一块的人都去使用React， 因为大多数人都是后端开发者。
更多的人并不了解 HTML CSS 怎么去工作，我们更愿意像写一个 Python 类一样去写一个组件。
Vue.js 给了我们太多的可选择性，上下兼顾，很容易被写成 AngularJS + React 的混合语法， 导致歧义。


Comparison 对比介绍
^^^^^^^^^^^^^^^^^^^^^^^^^

When building apps. we care those things best: 

当构建Web 应用时，我们比较注意的是一下几点：

- Basic components / 页面组件
- Tests / 测试
- L10N / 本地化
- Router / 路由
- Debug & Deploy / 调试和部署

Let's explore in React, Vue to see how to implement those features.

我们会去探索 React, Vue 来了解如何实现这些功能。

React
^^^^^^

    `React Sharing <React_Sharing.html>`_ 

Vue
^^^

    `Vue Sharing <Vue_Sharing.html>`_ 


UI Debug Tips
^^^^^^^^^^^^^^

.. _express_server:

Web Server with Express / 使用 Express 搭建Web Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Install  / 安装
    
.. code-block:: bash

    npm install body-parser
    npm install express

- Server / 搭建服务器

.. code-block:: bash

    const express = require('express');
    const bodyParser = require('body-parser');
    const app = express();

    app.use(bodyParser.urlencoded({ extended: false }))
    app.use(bodyParser.json());

    app.use(function(req, res, next) {
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
        next();
    });
    app.get('/rest/de_members', (req, res) => {
        res.send([
            "Fred",
            "Ben",
            "So on"
        ])
    });
    app.post('/rest/hello', (req, res) => {
        res.send({
            "message": 'welcome, ' + ( req.body.name || "undefined" ) + "!" 
        })
    });

    app.listen(3001, () => console.log('Example app listening on port 3001!'))


- Run :code:`node server.js`  / 运行服务器

.. figure:: /images/web/react_sharing_0002.png

Client: Restlet Client 

使用的测试工具: Restlet Client, Chrome 的插件，好东西，一生推... :)

