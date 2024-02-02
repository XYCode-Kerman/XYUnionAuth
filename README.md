# XYUnionAuth

## 这是什么？ | What's this?

XYUnionAuth是一个基于ABAC权限模型的用户登录与权限管理系统，原本是UnionSchool学校管理系统的一个附属项目，现已从UnionSchool项目中分离并作为单独模块开源。

XYUnionAuth提供了一系列高效易用的HTTP接口（文档：[XYUnionAuth](https://apifox.com/apidoc/shared-25d873c3-6bbd-48dd-8b56-65d52cb245f0)），同时适用于前端和后端。

## 如何使用？ | How to use?

首先，您需要克隆本项目并使用docker编译出镜像（不久后编译好的docker镜像将会上传至docker hub），然后，使用docker运行本项目的镜像。

我推荐您将`user/login/`和`user/register/`等接口在项目的前端中使用，而当您的项目涉及到权限管理时，则可以在后端调用`permissions/check_permission/`等接口以高效方便地验证用户的权限。
