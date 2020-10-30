# <div align="center">Đồ án môn học Máy học - Nhận diện biển số xe <br/> Nhóm 06</div>
# I) Mở đầu:
## 1) Phạm vi:
Trong nội dung của đồ án tập trung xử lý vào các đối tượng sau:
- Nhận diện các biển số xe của Việt Nam
- Nhận diện các biển số xe khi ra vào bãi gửi xe. Tức là tại một thời điểm chỉ có một biển số để nhận diện
## 2) Quy định về biển số xe Việt Nam:
Theo thông tư số 36/2010/TT-BCA của Bộ Công an ngày 12/10/2010:
- Biển số ô tô có 2 biển:
    - 1 biển gắn phía trước và 1 biển gắn phía sau xe phù hợp với vị trí nơi thiết kế lắp biển số của xe.
    - Kích thước như sau: 
        - Loại biển số dài có chiều cao 110 mm, chiều dài 470 mm
        - Loại biển số ngắn có chiều cao 200 mm, chiều dài 280 mm.
- Biển số xe mô tô, gồm 1 biển gắn phía sau xe
    - Kích thước: Chiều cao 140 mm, chiều dài 190 mm
- Cách bố trí chữ và số trên biển số trong nước: 
    - Hai số đầu là ký hiệu địa phương đăng ký xe
    - Tiếp theo là sê ri đăng ký (chữ cái) gồm 20 chữ cái A, B, C, D, E, F, G, H, K, L, M, N, P, S, T, U, V, X, Y, Z
    - Nhóm số thứ hai là thứ tự xe đăng ký gồm 05 chữ số tự nhiên từ 000.01 đến 999.99  
**Lưu ý:** Đây là những thông tin cơ bản cần thiết cho việc nhận diện biển số. Cụ thể có thể tham khảo thêm trong phần tham khảo <sup>[[01]](#L1)[[02]](#L2)</sup>  
-> Biển số xe Việt Nam gồm 9 kí tự (không tính dấu chấm) bao gồm 10 kí tự số từ 0 đến 9 và gồm 20 kí tự chữ , B, C, D, E, F, G, H, K, L, M, N, P, S, T, U, V, X, Y, Z
Các bước thực hiện:
# II) Các bước thực hiện:
<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262368986/in/dateposted-friend/" title="LPR_01"><img src="https://live.staticflickr.com/65535/50262368986_a0d67b7ccb_c.jpg" width="800" height="617" alt="LPR_01">
## 1) Tách biển số xe ra khỏi hình ảnh:
- Biển số xe được quy định bởi những quy tắc ở mục I.2 nên dựa vào các đặc trưng này để phân biệt với các đối tượng khác trong bức ảnh.
- Các bước chính gồm:
    - Định vị biển số xe trong ảnh
    - Dùng các phương pháp khác nhau để tách biển số xe ra khỏi ảnh
    - Tiến hành xử lý ảnh ( xoay, quay, co, dãn, phóng to, thu nhỏ, …)
## 2) Tách từng ký tự ra khỏi biển số:
- Gồm các bước:
    - Tiến hành phân ngưỡng để làm rõ các ký tự biển số với nền biển số
    - Tìm contour (đường viền) bao quanh các ký tự làm cơ sở để tách ký tự ra khỏi biển số
## 3) Điều chỉnh kích thước các ký tự cho phù hợp với từng mô hình nhận diện:  
Ứng với từng mô hình huấn luyện thì điều chỉnh ký tự tách được cho phù hợp để tăng tỷ lệ nhận diện
## 4) Nhận diện các ký tự của biển số:  
- Tạo tập dữ liệu huấn luyện
- Huấn luyện mô hình
- Nhận diện ký tự
- Điều chỉnh sửa lỗi nhận diện sai do phần tách ký tự
## 5) Kết quả thực hiện bằng code notebook:
<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262420781/in/album-72157715614150392/" title="LPR_02"><img src="https://live.staticflickr.com/65535/50262420781_42cc70abd4_c.jpg" width="800" height="587" alt="LPR_02"></a> 
# I) Các phương pháp áp dụng:
## 1) Tách biển số ra khỏi hình ảnh
- Sử dụng OpenCV
- Sử dụng YOLO (You Only Look Once): <sup>[[03]](#L3)[[04]](#L4)</sup>  
    - Yolo là một mô hình mạng CNN cho việc phát hiện, nhận dạng, phân loại đối tượng. 
    - Yolo được tạo ra từ việc kết hợp giữa các convolutional layers và connected layers.
    - Trong đó các convolutional layers sẽ trích xuất ra các feature của ảnh, còn full-connected layers sẽ dự đoán ra xác suất đó và tọa độ của đối tượng
- Sử dụng WPOD-NET (Warped Planar Object Detection Network): <sup>[[05]](#L5)[[06]](#L4)[[07]](#L3)[[08]](#L4)[[09]](#L3)[[15]](#L4)</sup> 
    - WPOD-NET được phát triển bằng cách sử dụng thông tin chuyên sâu từ YOLO, SSD và Spatial Transformer Networks (STN). 
    - YOLO và SSD thực hiện nhanh chóng nhiều lần phát hiện và nhận dạng đối tượng nhưng chúng không tính đến các biến đổi không gian, chỉ tạo các giới hạn hình chữ nhật cho mỗi lần phát hiện.
    - Ngược lại, STN có thể được sử dụng để phát hiện các vùng không phải hình chữ nhật, tuy nhiên nó không thể xử lý nhiều biến đổi cùng một lúc, chỉ thực hiện một chuyển đổi không gian duy nhất trên toàn bộ đầu vào
    - Tự động cắt và điều chỉnh cho ảnh biển số tốt nhất
## 2) Nhận diện ký tự
- Sử dụng CNN (Convolutional neural network) và SVM (Support vector machine) để nhận diện ký tự
    - Mô hình tổng quát:
<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262420711/in/album-72157715614150392/" title="LPR_04"><img src="https://live.staticflickr.com/65535/50262420711_24e2825cf0_c.jpg" width="768" height="631" alt="LPR_04"></a>
    - Layer đầu tiên là input layer, các layer ở giữa được gọi là hidden layer, layer cuối cùng được gọi là output layer. Các hình tròn được gọi là node.
    - Mỗi mô hình luôn có 1 input layer, 1 output layer, có thể có hoặc không các hidden layer. Tổng số layer trong mô hình được quy ước là số layer – 1 (Không tính input layer).
    - Convolutional layer: Mỗi hidden layer được gọi là fully connected layer, tên gọi theo đúng ý nghĩa, mỗi node trong hidden layer được kết nối với tất cả các node trong layer trước. Cả mô hình được gọi là fully connected neural network (FCN). 
    - Pooling layer: Pooling layer thường được dùng giữa các convolutional layer, để giảm kích thước dữ liệu nhưng vẫn giữ được các thuộc tính quan trọng. Kích thước dữ liệu giảm giúp giảm việc tính toán trong model. Có 2 loại pooling layer phổ biến là: max pooling và average pooling.
    - Fully connected layer: Sau khi ảnh được truyền qua nhiều convolutional layer và pooling layer thì model đã học được tương đối các đặc điểm của ảnh (ví dụ mắt, mũi, khung mặt,…) thì tensor của output của layer cuối cùng, kích thước H*W*D, sẽ được chuyển về 1 vector kích thước (H*W*D) -> Sau đó ta dùng các fully connected layer để kết hợp các đặc điểm của ảnh để ra được output của model.
- SVM:
    - Support Vector Machine (SVM) là một thuật toán thuộc nhóm Supervised Learning (Học có giám sát) dùng để phân chia dữ liệu (Classification) thành các nhóm riêng biệt.
# IV) Kết quả:
## 1) Nhận diện biển số trong ảnh - Tách biển số ra khỏi hình ảnh:
- Sử dụng OpenCV:
    - Tỷ lệ nhận diện:
        - Tỷ lệ nhận diện không cao

| Số lượng ảnh | Số lượng lỗi | Tỷ lệ lỗi |  
|--------------|--------------|-----------|   
|50 |	29|	57.99%|  
|100|	59|	59%   |  
|150|	89|	59.33%|

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262609562/in/album-72157715614150392/" title="LPR_05"><img src="https://live.staticflickr.com/65535/50262609562_92c4ef4565_z.jpg" width="640" height="294" alt="LPR_05"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262420626/in/album-72157715614150392/" title="LPR_06"><img src="https://live.staticflickr.com/65535/50262420626_33391399ba_z.jpg" width="640" height="261" alt="LPR_06"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262420631/in/album-72157715614150392/" title="LPR_07"><img src="https://live.staticflickr.com/65535/50262420631_7453834014_z.jpg" width="640" height="249" alt="LPR_07"></a>
- Chất lượng nhận diện:  
    \- Xác định chưa rõ vùng có biển số

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50261765328/in/album-72157715614150392/" title="LPR_08"><img src="https://live.staticflickr.com/65535/50261765328_50548e63e0.jpg" width="480" height="413" alt="LPR_08"></a>

    - Nhận diện nhầm

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50261766253/in/album-72157715614150392/" title="LPR_09"><img src="https://live.staticflickr.com/65535/50261766253_6336fdb981.jpg" width="480" height="394" alt="LPR_09"></a>

- Sử dụng YOLO (You Only Look Once):
    - Tỷ lệ nhận diện:
        - Tỷ lệ nhận diện cao

| Số lượng ảnh | Số lượng lỗi | Tỷ lệ lỗi |  
|--------------|--------------|-----------|   
|50 |	3|	6%|  
|100|	9|	9%|  
|150|	13|	8.67%|

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262421516/in/album-72157715614150392/" title="LPR_10"><img src="https://live.staticflickr.com/65535/50262421516_7df13ef168.jpg" width="500" height="229" alt="LPR_10"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262421501/in/album-72157715614150392/" title="LPR_11"><img src="https://live.staticflickr.com/65535/50262421501_6a51913398.jpg" width="500" height="231" alt="LPR_11"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262610397/in/album-72157715614150392/" title="LPR_12"><img src="https://live.staticflickr.com/65535/50262610397_978443c2fc.jpg" width="500" height="218" alt="LPR_12"></a>

- Chất lượng nhận diện:  
    \- Xác định chưa rõ vùng có biển số

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50261766203/in/album-72157715614150392/" title="LPR_13"><img src="https://live.staticflickr.com/65535/50261766203_0b6572a80f.jpg" width="500" height="386" alt="LPR_13"></a>

    - Xác định chưa rõ vùng có biển số
<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262421481/in/album-72157715614150392/" title="LPR_14"><img src="https://live.staticflickr.com/65535/50262421481_ef85bca307.jpg" width="500" height="310" alt="LPR_14"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262610327/in/album-72157715614150392/" title="LPR_15"><img src="https://live.staticflickr.com/65535/50262610327_582b85478c.jpg" width="479" height="273" alt="LPR_15"></a>

- Sử dụng WPOD-NET (Warped Planar Object Detection Network):
    - Tỷ lệ nhận diện:
        - Tỷ lệ nhận diện cao

| Số lượng ảnh | Số lượng lỗi | Tỷ lệ lỗi |  
|--------------|--------------|-----------|   
|50 |	10|	20%|  
|100|	13|	13%|  
|150|	16|	10.66%|

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50261766143/in/album-72157715614150392/" title="LPR_16"><img src="https://live.staticflickr.com/65535/50261766143_00640c7d8c.jpg" width="500" height="254" alt="LPR_16"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50261766093/in/album-72157715614150392/" title="LPR_17"><img src="https://live.staticflickr.com/65535/50261766093_d077224025.jpg" width="500" height="252" alt="LPR_17"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50261766073/in/album-72157715614150392/" title="LPR_18"><img src="https://live.staticflickr.com/65535/50261766073_24868149fc.jpg" width="500" height="253" alt="LPR_18"></a>

- Chất lượng nhận diện:
    - Chất lượng nhận diện tốt.
    - Xác định rõ vùng có biển số
    - Không bị mất nét

- Nhận diện được biển số ngắn:

| Số lượng ảnh | Số lượng lỗi | Tỷ lệ lỗi |  
|--------------|--------------|-----------|   
|50 |	9|	18%|  
|100|	6|	6%|  
|150|	3|	2%|

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262421411/in/album-72157715614150392/" title="LPR_19"><img src="https://live.staticflickr.com/65535/50262421411_2bbf117bf2.jpg" width="500" height="330" alt="LPR_19"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262610247/in/album-72157715614150392/" title="LPR_20"><img src="https://live.staticflickr.com/65535/50262610247_6821af440d.jpg" width="500" height="328" alt="LPR_20"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262421366/in/album-72157715614150392/" title="LPR_21"><img src="https://live.staticflickr.com/65535/50262421366_a03fbf6a7d.jpg" width="500" height="329" alt="LPR_21"></a>
-> Sử dụng nhận diện biển số bằng WPODNET và YOLO cho bước tiếp theo

## 2) Nhận diện ký tự:
- Sử dụng CNN:
    - Biển dài

| Số lượng ảnh - Model | Số lượng lỗi | Tỷ lệ lỗi | Ghi chú |   
|--------------|--------------|-----------| ---------|  
|50 - 5k |	13|	26%| 20% là do WPODNET & OpenCV |
|100 - 5k|	24|	24%|  15% là do WPODNET & OpenCV (Có xử lý để tách ký tự sai nhưng vẫn nhận diện đúng) |
|150 - 3k|	30|	20%| 18% là do WPODNET & OpenCV (Có xử lý để tách ký tự sai nhưng vẫn nhận diện đúng) |
|150 - 3k |	55|	36.66%| 18% là do WPODNET & OpenCV (Có xử lý để tách ký tự sai nhưng vẫn nhận diện đúng) |
|150 - 7k |	53|	35.33%| 18% là do WPODNET & OpenCV (Có xử lý để tách ký tự sai nhưng vẫn nhận diện đúng) |
|150 - 10k | 60| 40%| 18% là do WPODNET & OpenCV (Có xử lý để tách ký tự sai nhưng vẫn nhận diện đúng) |

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262421201/in/album-72157715614150392/" title="LPR_31"><img src="https://live.staticflickr.com/65535/50262421201_e93f16cc4e.jpg" width="500" height="178" alt="LPR_31"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262610082/in/album-72157715614150392/" title="LPR_32"><img src="https://live.staticflickr.com/65535/50262610082_7b515779c5.jpg" width="500" height="172" alt="LPR_32"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262421196/in/album-72157715614150392/" title="LPR_33"><img src="https://live.staticflickr.com/65535/50262421196_5884a91b4d.jpg" width="500" height="175" alt="LPR_33"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262610017/in/album-72157715614150392/" title="LPR_34"><img src="https://live.staticflickr.com/65535/50262610017_c50f2a8ec9.jpg" width="500" height="177" alt="LPR_34"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262610002/in/album-72157715614150392/" title="LPR_35"><img src="https://live.staticflickr.com/65535/50262610002_d33c6d2fc5.jpg" width="500" height="184" alt="LPR_35"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50261765858/in/album-72157715614150392/" title="LPR_36"><img src="https://live.staticflickr.com/65535/50261765858_551b92c625.jpg" width="500" height="172" alt="LPR_36"></a>

    - Biển ngắn

| Số lượng ảnh | Số lượng lỗi | Tỷ lệ lỗi | Ghi chú |   
|--------------|--------------|-----------| ---------|
|50 |	19|	38%| 24% là do WPODNET & OpenCV |
|100 |	25|	25%| 11% là do WPODNET & OpenCV |
|150 |	33|	22%| 6% là do WPODNET & OpenCV |

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262609982/in/album-72157715614150392/" title="LPR_37"><img src="https://live.staticflickr.com/65535/50262609982_709d299a7d.jpg" width="500" height="169" alt="LPR_37"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262421106/in/album-72157715614150392/" title="LPR_38"><img src="https://live.staticflickr.com/65535/50262421106_46b34ea872.jpg" width="500" height="181" alt="LPR_38"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262421086/in/album-72157715614150392/" title="LPR_39"><img src="https://live.staticflickr.com/65535/50262421086_3113413b4a.jpg" width="500" height="178" alt="LPR_39"></a>

- Sử dụng SVM:  
    \- Biển dài:

| Số lượng ảnh - Model | Số lượng lỗi | Tỷ lệ lỗi | Ghi chú |   
|--------------|--------------|-----------| ---------|  
|50 - 99 |	35|	70%| 20% là do WPODNET & OpenCV |
|100 - 99|	70|	70%|  15% là do WPODNET & OpenCV (Có xử lý để tách ký tự sai nhưng vẫn nhận diện đúng) |
|150 - 99| 110|	73.33%| 18% là do WPODNET & OpenCV (Có xử lý để tách ký tự sai nhưng vẫn nhận diện đúng) |
|150 - 50 |	116| 73.33%| 18% là do WPODNET & OpenCV (Có xử lý để tách ký tự sai nhưng vẫn nhận diện đúng) |
|150 - 500 | 116| 73.33%| 18% là do WPODNET & OpenCV (Có xử lý để tách ký tự sai nhưng vẫn nhận diện đúng) |
|150 - 10k | 137| 91.33%| 18% là do WPODNET & OpenCV (Có xử lý để tách ký tự sai nhưng vẫn nhận diện đúng) |

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50261765803/in/album-72157715614150392/" title="LPR_40"><img src="https://live.staticflickr.com/65535/50261765803_2d168ecc9b.jpg" width="500" height="202" alt="LPR_40"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50261765773/in/album-72157715614150392/" title="LPR_41"><img src="https://live.staticflickr.com/65535/50261765773_dfb6eef5f0.jpg" width="500" height="171" alt="LPR_41"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262609942/in/album-72157715614150392/" title="LPR_42"><img src="https://live.staticflickr.com/65535/50262609942_42c048406e.jpg" width="500" height="181" alt="LPR_42"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50261765748/in/album-72157715614150392/" title="LPR_43"><img src="https://live.staticflickr.com/65535/50261765748_1323692b36.jpg" width="500" height="169" alt="LPR_43"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262609907/in/album-72157715614150392/" title="LPR_44"><img src="https://live.staticflickr.com/65535/50262609907_28dc651928.jpg" width="500" height="182" alt="LPR_44"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262609892/in/album-72157715614150392/" title="LPR_45"><img src="https://live.staticflickr.com/65535/50262609892_532b4fdb2f.jpg" width="500" height="175" alt="LPR_45"></a>

    - Biển ngắn

| Số lượng ảnh | Số lượng lỗi | Tỷ lệ lỗi | Ghi chú |   
|--------------|--------------|-----------| ---------|
|50 |	46|	92%| 24% là do WPODNET & OpenCV |
|100 |	91|	91%| 11% là do WPODNET & OpenCV |
|150 |	136| 90.66%| 6% là do WPODNET & OpenCV |

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262420946/in/album-72157715614150392/" title="LPR_46"><img src="https://live.staticflickr.com/65535/50262420946_5ccc7c1745.jpg" width="500" height="176" alt="LPR_46"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262420851/in/album-72157715614150392/" title="LPR_47"><img src="https://live.staticflickr.com/65535/50262420851_05abbf0fe2.jpg" width="500" height="168" alt="LPR_47"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262609747/in/album-72157715614150392/" title="LPR_48"><img src="https://live.staticflickr.com/65535/50262609747_a517c4a5e2.jpg" width="500" height="175" alt="LPR_48"></a>

# V) Mở rộng – Cải tiến:
- Nhận diện ở phạm vi rộng hơn:
    - Nhận diện các biển số xe nước ngoài
    - Nhận diện được các biển số xe khi tham gia giao thông (nhận diện được nhiều biển số)
    - Nhận diện được trong video giao thông
- Phương pháp sử dụng:
    - Điều chỉnh code tách ký tự biển số sử dụng OpenCV để tách ký tự của biển số YOLO tốt hơn
    - Điều chỉnh phần tách ký tự biển số để kết quả tốt hơn khi nhận diện bằng SVM

# VI) Kết luận:
- Nhận diện biển số xe phụ thuộc vào nhiều yếu tố. Trong đó yếu tố chất lượng ảnh đầu vào ảnh hưởng lớn kết quả. Dù mô hình nhận diện có tốt đến đâu nhưng ảnh không phát hiện được biển số hay tách ký tự sai thì nhận diện đều cho kết quả sai.
- Mô hình SVM không phải là không tốt mà do việc tiền xử lý chưa tối ưu cho SVM mà tập trung cho CNN nên kết quả mới thấp

# VII) Source code:
Do file source code chứa các file train dữ liệu và model kích thước lớn nên upload lên google drive. 
http://bit.ly/VMHLPR96 
Cấu trúc thư mục như sau:  
<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262609742/in/album-72157715614150392/" title="LPR_49"><img src="https://live.staticflickr.com/65535/50262609742_e901139251.jpg" width="500" height="116" alt="LPR_49"></a>

<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50261765523/in/album-72157715614150392/" title="LPR_50"><img src="https://live.staticflickr.com/65535/50261765523_b262399519.jpg" width="500" height="279" alt="LPR_50"></a>

# VIII) Tham khảo:
<a name="L1"></a>
[01] - https://tintucvietnam.vn/quy-dinh-ve-bien-so-xe-d161272.html  
<a name="L2"></a>
[02] - https://danluat.thuvienphapluat.vn/cach-phan-biet-cac-loai-bien-so-xe-170243.aspx  
<a name="L3"></a>
[03] - https://viblo.asia/p/tim-hieu-ve-yolo-trong-bai-toan-real-time-object-detection-yMnKMdvr57P  
<a name="L4"></a>
[04]  - https://forum.machinelearningcoban.com/t/object-detection-yolo/503  
<a name="L5"></a>
[05] - https://ainoodle.vn/2019/11/20/nhan-dien-bien-so-xe-chuong-2-phat-hien-bien-so-xe-bang-pretrain-wpod-net/  
<a name="L6"></a>
[06] - http://openaccess.thecvf.com/content_ECCV_2018/papers/Sergio_Silva_License_Plate_Detection_ECCV_2018_paper.pdf  
<a name="L7"></a>
[07] - http://www.programmersought.com/article/60841505614/  
<a name="L8"></a>
[08] - https://github.com/sergiomsilva/alpr-unconstrained  
<a name="L9"></a>
[09] - https://www.cnblogs.com/greentomlee/p/10863363.html  
<a name="L10"></a>
[10] - https://github.com/keras-team/keras/blob/master/examples/cifar10_cnn.py  
<a name="L11"></a>
[11] - https://www.phamduytung.com/blog/2019-05-05-deep-learning-dropout/  
<a name="L12"></a>
[12] - https://nttuan8.com/bai-6-convolutional-neural-network  
<a name="L13"></a>
[13] - https://1upnote.me/post/2018/10/ds-ml-svm/  
<a name="14"></a>
[14] - https://machinelearningcoban.com/2017/03/04/overfitting/  
<a name="L15"></a>
[15] – https://www.researchgate.net/figure/Detailed-WPOD-NET-architecture_fig3_327861610
