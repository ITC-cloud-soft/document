# 1. Kong Gateway

## 1.1. 概要

　Kong Gatewayは、Kong Inc.が提供するソフトウェアで、マイクロサービスと分散アーキテクチャに最適化されたAPIゲートウェイです。オープンソース版と商用版があり、どちらもAPIゲートウェイ機能を持っています。Kong GatewayはAPIのリバースプロキシとして機能し、Webアクセスを受け取り、それをバックエンドのAPI実行サーバーに転送します。これにより、複数のマイクロサービス型のAPI実行サーバーを一元管理することができます。

Kong Gatewayには、認証、アクセス制限、レート制限、監視などの機能があります。また、プラグイン（Kong Plugin Hub）を使用することで、その機能を拡張することができます。

## 1.2. オープンソース版と商用版の比較

参照資料：[Kong Gateway for every stage
of your API journey](https://konghq.com/products/kong-gateway)

![Alt text](images/stage_diff_1.png)
![Alt text](images/stage_diff_2.png)
![Alt text](images/stage_diff_3.png)
![Alt text](images/stage_diff_4.png)
![Alt text](images/stage_diff_5.png)
![Alt text](images/stage_diff_6.png)

## 1.3. 構築(Kubernetes)

※Open Source版のKong Gatewayの機能は少ないので、本番には適用しないと思います。SaaS版の構築方法を次のように説明します。

参照サイト：[Kong in K8s](https://docs.konghq.com/gateway/3.5.x/install/kubernetes/)

### 1.3.1 Hybrid Modeの構成図

![Alt text](images/hybrid_mode.png)

**メリット：**

* 展開の柔軟性： ユーザーは、DPグループごとにローカルクラスタ化データベースを用意することなく、データプレーンのグループを異なるデータセンター、地域、ゾーンに展開できます。
* 信頼性の向上： データベースの可用性がデータプレーンの可用性に影響することはありません。各DPはコントロール・プレーンから受け取った最新のコンフィグレーションをローカルのディスク・ストレージにキャッシュするため、CPノードがダウンしてもDPノードは機能し続けます。
  * CPがダウンしている間、DPノードは常に通信の再確立を試みます。
  * CPがダウンしている間にDPノードを再起動しても、プロキシトラフィックは正常なままです。
* トラフィックの削減： データベースへの直接接続が必要なのはCPノードのみであるため、データベースとのトラフィック量が大幅に削減されます。
* セキュリティの向上： DPノードの1つが侵害されても、攻撃者はKongクラスタの他のノードに影響を与えることができません。
* 管理の容易さ： 管理者はCPノードとやり取りするだけで、Kongクラスタ全体のステータスを制御および監視できます。

**重要：**
Kong クラスターがあるからといって、クライアント トラフィックが Kong ノード間で負荷分散されるわけではありません。トラフィックを分散するために、Kongノードの前にロードバランサーが必要です。代わりに、Kong クラスターは、これらのノードが同じ構成を共有することを意味します。
[What a Kong cluster does and doesn’t do](https://docs.konghq.com/gateway/latest/production/deployment-topologies/traditional/)

### 1.3.2 Data Plane Node(DP)の作成

１．[Kong Manager](https://signin.cloud.konghq.com/)へログインします

![Alt text](images/login.png)

２．Gateway ManagerからCPを選択します

![Alt text](images/cp_select.png)

3．DP作成コードの参照

(1) URL確認
![Alt text](images/cp_base_url.png)

(2) 上記のURLの「overview」を「configuration」に変更します
![Alt text](images/dp_create.png)

(3) 「Create a Data Plane Node」から実行コマンドをコピーして環境にて叩きます

### 1.3.3 サービス、ルートの登録

Admin APIより：[Services and Routes](https://docs.konghq.com/gateway/3.5.x/get-started/services-and-routes/)

Kong Managerより：[Services and Routes](https://docs.konghq.com/gateway/3.5.x/kong-manager/get-started/services-and-routes/)

**構成図：**
![Alt text](images/service_route.png)

(1) Service設定(業務アプリケーション)
![Alt text](images/config_service.png)

(2) Route設定(アクセスエンドポイント)
![Alt text](images/config_route.png)

### 1.3.4 Load balancing

Admin APIより：[Load Balancing](https://docs.konghq.com/gateway/3.5.x/get-started/load-balancing/)

Kong Managerより：[Load Balancing](https://docs.konghq.com/gateway/3.5.x/kong-manager/get-started/load-balancing/)

**構成図：**
![Alt text](images/load_balance.png)

(1) Load balancingの設定
![Alt text](images/upstream.png)

## 1.4. Firewall

### 1.4.1 コンフィグファイルより

参照サイト：[Firewall](https://docs.konghq.com/gateway/latest/production/networking/firewall/#firewall)

### 1.4.2 IP Restrictionプラグインより

参照サイト：[IP Restriction Configuration](https://docs.konghq.com/hub/kong-inc/ip-restriction/configuration/)

IPアドレスを許可または拒否することで、サービスやルートへのアクセスを制限します。単一のIP、複数のIP、または10.10.10.0/24のようなCIDR表記の範囲を使用できます。

プラグインはIPv4とIPv6アドレスをサポートしています。

## 1.5. CORS

参照サイト：[CORS Configuration](hhttps://docs.konghq.com/hub/kong-inc/cors/configuration/)

CORS（Cross-Origin Resource Sharing）の設定はCORSプラグインを使用して行います。サービスごと、ルートごとまたは全体のCORS設定はできます。

* CORSプラグインの追加
![Alt text](images/select_cors.png)

* CORSプラグインの設定
![Alt text](images/configure_cors.png)
※各項目にはどんな値を設定するのは下記のサイトを参照してください。
[Kong: CORS Configuration](https://docs.konghq.com/hub/kong-inc/cors/configuration/)
[MDN: Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)


<style>
p:has(> img){
    display: grid;
}
</style>
