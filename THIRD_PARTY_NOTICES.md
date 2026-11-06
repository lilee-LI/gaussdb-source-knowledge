# 第三方组件

离线依赖为 NetworkX 3.7 与 pypdf 6.10.2。随包 wheel 保留其许可证和发行元数据，版本及 SHA-256 见 [依赖锁文件](wheels/common-py312/requirements.lock)。Wiki 相关许可证见 [licenses](licenses/)。

Linux 产图端使用 libclang 18.1.1 的 PyPI x86_64 与 aarch64 wheel；按平台只安装一个。[x86_64 锁文件](wheels/ecs-linux-x64/requirements.lock) · [aarch64 锁文件](wheels/ecs-linux-arm64/requirements.lock) · [上游发行](https://pypi.org/project/libclang/18.1.1/)。

Clang 18 内置头文件来自 Ubuntu 的 libclang-common-18-dev 1:18.1.3-1ubuntu1，按原相对路径归档在 wheels/ecs-resource/clang18-headers.tar.xz。分发许可与各文件说明见[随包版权文件](wheels/ecs-resource/COPYRIGHT)。

测试样本使用本项目的微型 C++ 源码和合成研究记录。测试运行时在临时目录创建 SQLite。公开 openGauss 的仓库与实验输入由验证环境提供，不随本代码仓分发。
