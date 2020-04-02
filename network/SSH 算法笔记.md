# SSH 算法笔记

本文把学习 SSH算法时遇到的名词罗列出来，做个笔记分享出来。里面的解释和引文都是来自其他作者公开的内容。

如果对这些算法感兴趣，想进一步了解，推荐廖雪峰的网站[加密与安全](https://www.liaoxuefeng.com/wiki/1252599548343744/1255943717668160)

#### 密钥交换算法Key Exchange Algorithm:

解决了密钥在双方不直接传递密钥的情况下完成密钥交换

研究过的算法

- curve25519-sha256
- curve25519-sha256@libssh.org

Curve25519 2005年由 [Daniel J. Bernstein](https://en.wikipedia.org/wiki/Daniel_J._Bernstein)发布，2013年后由于 NSA 后门丑闻[https://zh.wikipedia.org/wiki/Bullrun_(NSA%E8%A8%88%E7%95%AB)](https://zh.wikipedia.org/wiki/Bullrun_(NSA計畫))后大家对 Curve25519兴趣增加。

Curve25519是最快的椭圆曲线算法之一，而且没有被任何专利保护。

- diffie-hellman-group16-sha512

  - 参考https://blog.51cto.com/wchrt/1649839

    **diffie-hellman-group-sha512**的整个过程中一共要用到的秘钥交换算法有：**diffie-hellman、sha512、ssh-rsa**

    Diffie-Hellman (DH) groups决定了key 的强度。key越大越安全，但是计算越慢。

  - DH Group 1: 768-bit group
  - DH Group 2: 1024-bit group
  - DH Group 5: 1536-bit group
  - DH Group 14: 2048-bit group
  - DH Group 15: 3072-bit group
  - DH Group 19: 256-bit elliptic curve group
  - DH Group 20: 384-bit elliptic curve group

### 密钥算法Key  Algorithm:

用于生成密钥对。

 **ssh-ed25519-cert-v01@openssh.com**

**ssh-ed25519**

ed25519也是椭圆曲线算法，比RSA 安全性高，而且性能也好

参考 :https://ed25519.cr.yp.to/

- **Fast single-signature verification.**
- **Even faster batch verification.** 
- **Very fast signing.** 
- **Fast key generation.** 
- **High security level.** 
- **Small signatures.**
- Small keys

### 加密算法Cipher algorithms

- **chacha20-poly1305@openssh.com**

ChaCha20-Poly1305是Google所采用的一种新式加密算法，混合了 ChaCha20和 Poly1305， 用于替代 RC4(2015年被比利时学者破解了https://zh.wikipedia.org/wiki/RC4)

ChaCha20是流加密，以字节为单位进行加密。

Poly1305消息认证码： 消息认证码（带密钥的[Hash函数](https://baike.baidu.com/item/Hash函数)）:密码学中，通信实体双方使用的一种验证机制，保证消息[数据完整性](https://baike.baidu.com/item/数据完整性)的一种工具。[构造方法](https://baike.baidu.com/item/构造方法)由M.Bellare提出，安全性依赖于Hash函数，故也称带密钥的Hash函数。消息认证码是基于密钥和消息摘要所获得的一个值，可用于数据源发认证和完整性校验。

参考：https://baike.baidu.com/item/chacha20-poly1305



#### 消息认证码Mac algorithm

HMAC 是一种使用单向散列函数来构造消息认证码的方法，HMAC 中的 H 是 Hash 的意思。

https://halfrost.com/message_authentication_code/#hmac



