# python_licenseplaterecognition
Project Python License Plate Recognition
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
 Biển số xe Việt Nam gồm 9 kí tự (không tính dấu chấm) bao gồm 10 kí tự số từ 0 đến 9 và gồm 20 kí tự chữ , B, C, D, E, F, G, H, K, L, M, N, P, S, T, U, V, X, Y, Z
Các bước thực hiện:
# II) Các bước thực hiện:
<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262368986/in/dateposted-friend/" title="LPR_01"><img src="https://live.staticflickr.com/65535/50262368986_a0d67b7ccb_c.jpg" width="800" height="617" alt="LPR_01"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>  
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
<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262420781/in/album-72157715614150392/" title="LPR_02"><img src="https://live.staticflickr.com/65535/50262420781_42cc70abd4_c.jpg" width="800" height="587" alt="LPR_02"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>  
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
<a data-flickr-embed="true" href="https://www.flickr.com/photos/159324265@N07/50262420711/in/album-72157715614150392/" title="LPR_04"><img src="https://live.staticflickr.com/65535/50262420711_24e2825cf0_c.jpg" width="768" height="631" alt="LPR_04"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>
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

# IX) Tham khảo:
<a name="L1"></a>
[01] - https://tintucvietnam.vn/quy-dinh-ve-bien-so-xe-d161272.html  
<a name="L2"></a>
[02] - https://danluat.thuvienphapluat.vn/cach-phan-biet-cac-loai-bien-so-xe-170243.aspx
