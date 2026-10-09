ACK = '''Nhóm xin gửi lời cảm ơn đến thầy Nguyễn Thành Ngô, giảng viên học phần Big Data, vì những kiến thức thầy đã truyền đạt trong quá trình giảng dạy. Nội dung học phần cung cấp cơ sở để nhóm tìm hiểu các phương pháp xử lý dữ liệu lớn và vận dụng vào bài toán phân tích, dự báo điện năng tiêu thụ.

Báo cáo có thể còn thiếu sót về nội dung và cách trình bày. Nhóm mong nhận được ý kiến góp ý của thầy để điều chỉnh và hoàn thiện báo cáo.

Nhóm xin chân thành cảm ơn thầy.'''

INTRO = {
1: '''Dữ liệu điện năng ghi nhận theo thời gian cho phép mô tả mức sử dụng điện và xây dựng mô hình dự báo từ các quan sát quá khứ. Khi phép đo được thu thập theo phút trong nhiều năm, quá trình phân tích cần kiểm tra chất lượng bản ghi, thống nhất đơn vị và tổng hợp dữ liệu trước khi sử dụng cho mô hình. Các khoảng mất phép đo có thể làm sai lệch tổng điện năng nếu bị thay bằng 0 hoặc được xem như những giờ đầy đủ.

Đề tài sử dụng bộ UCI Individual Household Electric Power Consumption của một hộ gia đình tại Pháp. Apache Flink thực hiện xử lý tệp hữu hạn và tổng hợp theo giờ; Python xây dựng mô hình dự báo; dashboard cung cấp chức năng phân tích và suy luận từ kết quả đã lưu. Cách tổ chức này cho phép kiểm tra riêng tính đúng đắn của dữ liệu sau xử lý, mô hình và giao diện.''',
2: '''Mục tiêu của đề tài là phân tích điện năng tiêu thụ theo thời gian và dự báo điện năng của một giờ kế tiếp, đơn vị kWh. Các nhiệm vụ gồm khảo sát dữ liệu gốc, xây dựng quy tắc chất lượng, tổng hợp bằng Flink SQL BATCH, phân tích sự thay đổi theo thời gian và đánh giá mô hình dự báo trên một giai đoạn kiểm thử cố định.

Sản phẩm ứng dụng gồm ba tab Tổng quan, Phân tích và Dự báo. Các chỉ số và biểu đồ sử dụng dữ liệu đã xử lý; dự báo sử dụng mô hình HistGradientBoostingRegressor đã huấn luyện và lưu. Kết quả được so sánh với Naive và Seasonal Naive 24 giờ bằng MAE và RMSE, không sử dụng tỷ lệ phần trăm độ chính xác chung cho bài toán hồi quy.''',
3: '''Đối tượng nghiên cứu là chuỗi điện năng của một hộ gia đình tại Sceaux, Pháp, ghi nhận từ ngày 16/12/2006 đến ngày 26/11/2010. Dữ liệu gồm 2.075.259 bản ghi theo phút với chín cột. Biến mục tiêu được xây dựng từ công suất tác dụng trung bình từng phút, không phải từ việc cộng trực tiếp các nhóm đo phụ.

Phạm vi thực nghiệm là dự báo một bước cuốn chiếu trên dữ liệu lịch sử: tại mỗi mốc, mô hình sử dụng những quan sát thực tế đã có của các giờ trước để dự báo khoảng giờ kế tiếp. Ứng dụng không kết nối công tơ trực tiếp, không dự báo mức sử dụng điện hiện tại và không mở rộng sang nhiều hộ. Flink được chạy trên một môi trường WSL2 cục bộ; kết quả không chứng minh khả năng mở rộng hoặc vận hành production nhiều máy.''',
4: '''Quy trình thực hiện gồm kiểm tra toàn bộ dữ liệu gốc, xác thực dấu thời gian và giá trị số, tổng hợp theo giờ bằng Flink, rồi đối chiếu kết quả với phép tính độc lập. Dữ liệu giờ được giữ trên trục thời gian liên tục, có cờ đầy đủ và giá trị thiếu rõ ràng.

Tập đặc trưng gồm các giá trị trễ, trung bình quá khứ và thông tin lịch. Train, Validation và Test được chia theo thời gian trước khi lọc mẫu hợp lệ. Mô hình học từ Train, được lựa chọn qua Validation và giữ nguyên khi đánh giá Test. Kiểm thử ứng dụng bao gồm chức năng, trường hợp thiếu dữ liệu, lỗi nguồn, suy luận và khởi động/phục hồi dịch vụ trong phạm vi cục bộ.''',
5: '''Báo cáo gồm năm chương. Chương 1 xác định bối cảnh, bài toán và hướng tiếp cận. Chương 2 trình bày cơ sở chuỗi thời gian, dự báo và công nghệ sử dụng. Chương 3 khảo sát, tổng hợp và phân tích dữ liệu UCI. Chương 4 mô tả tập đặc trưng, mô hình và kết quả đánh giá. Chương 5 trình bày hệ thống xử lý dữ liệu, dashboard và phạm vi kiểm thử. Phần kết luận tổng hợp kết quả, hạn chế và hướng phát triển.'''
}

CH1_REPLACEMENTS = {
226: '''Đối với bộ dữ liệu Individual Household Electric Power Consumption được chọn cho đề tài, dữ liệu gốc gồm 2.075.259 bản ghi theo phút của một hộ gia đình. Apache Flink SQL BATCH kiểm tra bản ghi và tổng hợp công suất tác dụng thành điện năng theo giờ. Chuỗi kết quả được dùng cho phân tích và dự báo giờ kế tiếp bằng Python. Lưu trữ, xử lý dữ liệu và huấn luyện mô hình là các thành phần riêng; sử dụng bộ máy xử lý phân tán không đồng nghĩa mô hình cũng được huấn luyện phân tán.''',
230: '''Dữ liệu được kiểm tra về thời gian ghi nhận, đơn vị đo, giá trị thiếu và bản ghi trùng. Từ công suất tác dụng trung bình theo phút, quy trình tính điện năng của từng giờ, đơn vị kWh. Những giờ đủ 60 bản ghi, 60 dấu thời gian phút khác nhau và 60 phép đo công suất hợp lệ được sử dụng làm điện năng giờ đầy đủ. Các giờ còn lại được đánh dấu; tổng điện năng quan sát được giữ riêng, không thay cho điện năng của cả giờ.''',
231: '''Nhiệm vụ phân tích mô tả mức tiêu thụ theo giờ trong ngày, ngày trong tuần, tháng và ba nhóm đo phụ. Nhiệm vụ dự báo sử dụng điện năng của giờ kế tiếp làm biến mục tiêu. Với khoảng giờ bắt đầu tại s, mốc phát dự báo là s và quan sát mới nhất được dùng thuộc khoảng giờ trước đó. Đặc trưng không chứa điện năng của giờ đang cần dự báo.''',
232: '''Dữ liệu được chia theo thứ tự thời gian thành Train, Validation và Test. Mô hình HistGradientBoostingRegressor được huấn luyện trên Train, lựa chọn thông qua Validation và giữ nguyên khi đánh giá Test. Naive và Seasonal Naive 24 giờ là hai phương pháp đối chiếu; MAE và RMSE được tính trên cùng các mốc hợp lệ. Apache Flink đảm nhiệm xử lý dữ liệu lịch sử, còn huấn luyện và suy luận bằng Python là thành phần riêng.'''
}

CH2_REPLACE = {
3: 'Dữ liệu chuỗi thời gian (Time Series Data) là tập hợp các quan sát được sắp xếp theo thời điểm ghi nhận. Các mốc có thể cách đều như phút, giờ, ngày hoặc có khoảng cách không đều tùy nguồn. Trong phân tích, thứ tự và khoảng cách thời gian cần được bảo toàn để diễn giải quan hệ giữa các quan sát.',
4: 'Một chuỗi thời gian có thể biểu diễn bằng dãy giá trị x₁, x₂, …, xₜ, trong đó xₜ là quan sát tại thời điểm t. Nhiều chuỗi có quan hệ phụ thuộc giữa giá trị hiện tại và quá khứ. Dữ liệu dạng bảng không mặc nhiên có các quan sát độc lập; giả định độc lập và cùng phân phối chỉ phù hợp với một số bài toán hoặc phương pháp cụ thể.',
5: 'Trong Big Data, dữ liệu chuỗi thời gian có thể được xử lý từ tệp lịch sử hoặc từ luồng cập nhật. Các đặc trưng về khối lượng, tốc độ và sự đa dạng phụ thuộc vào quy mô nguồn:',
6: 'Volume (Khối lượng): Các phép đo tích lũy qua thời gian hoặc đến từ nhiều nguồn tạo thành tập dữ liệu lớn cần tổ chức lưu trữ và xử lý.',
7: 'Velocity (Tốc độ): Nguồn có thể phát sinh dữ liệu liên tục; yêu cầu độ trễ xử lý phụ thuộc bài toán. Tệp UCI của đề tài được đọc ở chế độ BATCH, không đặt yêu cầu xử lý từng bản ghi theo thời gian thực.',
10: 'Một chuỗi thời gian có thể được mô tả bằng xu hướng, mùa vụ, chu kỳ và phần dư. Không phải chuỗi nào cũng có đủ các thành phần này; sự tồn tại và hình thức của chúng cần được kiểm tra trên dữ liệu:',
16: 'Mô hình cộng tính (Additive Model): Giá trị chuỗi được mô tả bằng tổng các thành phần. Dạng này phù hợp khi biên độ mùa vụ không thay đổi nhiều theo mức của chuỗi.',
17: 'Mô hình nhân tính (Multiplicative Model): Các thành phần được kết hợp bằng phép nhân; thường được xem xét với chuỗi dương khi biên độ mùa vụ thay đổi theo mức của chuỗi.',
20: 'Tính không dừng có thể ảnh hưởng tới các phương pháp có giả định dừng và cách diễn giải quan hệ thống kê. Yêu cầu xử lý phụ thuộc mô hình; không phải mọi mô hình dự báo đều cần cùng một phép biến đổi để tạo tính dừng.',
22: 'ACF đo tương quan giữa chuỗi và các giá trị trễ; PACF đo tương quan tại một độ trễ sau khi loại ảnh hưởng tuyến tính của các độ trễ trung gian. Các công cụ này hỗ trợ lựa chọn một số mô hình tự hồi quy, nhưng không được sử dụng để quyết định cấu hình HGB trong thực nghiệm của đề tài.',
26: 'Forecasting Horizon là khoảng cách từ mốc dự báo đến thời điểm cần ước lượng. Horizon xác định nhiệm vụ và thông tin có thể sử dụng; sai số còn phụ thuộc dữ liệu, mô hình và phương pháp đánh giá.',
27: 'Dự báo một bước (One-step Ahead): Ước lượng giá trị của khoảng tiếp theo từ thông tin quá khứ đã quan sát. Khi đánh giá cuốn chiếu, tại mỗi mốc có thể bổ sung quan sát thực tế mới nhưng không nhất thiết huấn luyện lại mô hình.',
29: 'Dự báo nhiều bước (Multi-step Ahead): Ước lượng nhiều khoảng tương lai từ một mốc ban đầu. Sai số và yêu cầu đặc trưng phụ thuộc cách mô hình tạo các bước tiếp theo.',
34: 'Dự báo đầu ra đồng thời (Joint/Multi-output): Một mô hình sinh nhiều giá trị tương lai cùng lúc. Phương pháp có thể sử dụng mô hình đa đầu ra hoặc học sâu, không chỉ giới hạn ở mạng nơ-ron.',
36: 'Tiền xử lý xác định cách diễn giải giá trị thiếu, ngoại lai, tần suất và đơn vị đo trước khi mô hình hóa. Chính sách cần phù hợp với thông tin sẵn có tại mốc dự báo.',
40: 'Backward Fill: Điền giá trị thiếu bằng quan sát phía sau. Cách này chỉ phù hợp với một số mục đích hồi cứu; khi giá trị tương lai chưa có tại mốc dự báo, dùng nó để tạo đặc trưng gây rò rỉ dữ liệu, kể cả trong thực nghiệm offline.',
41: 'Nội suy tuyến tính hoặc spline: Ước lượng điểm thiếu từ các quan sát lân cận. Nếu sử dụng điểm phía tương lai, phép nội suy không còn là biến đổi chỉ dựa trên quá khứ tại mốc dự báo.',
44: 'Z-score, khoảng tứ phân vị và thống kê cửa sổ có thể hỗ trợ phát hiện các giá trị khác biệt. Một giá trị điện năng lớn không mặc nhiên là lỗi đo. Việc xóa, cắt ngưỡng hoặc thay thế cần có căn cứ nghiệp vụ và đánh giá tác động, không chỉ dựa vào một ngưỡng thống kê.',
46: 'Lấy mẫu lại (Resampling) đưa dữ liệu về tần suất phù hợp bằng tổng hợp hoặc tái lập trục thời gian. Hàm tổng hợp phải tuân theo đơn vị: công suất trung bình từng phút được nhân với thời lượng để tính điện năng, không được cộng kW rồi đổi tên thành kWh. Tăng tần suất không tự tạo thêm thông tin đo thực tế.',
48: 'Min-Max Scaling thay đổi thang giá trị; StandardScaler chuẩn hóa theo trung bình và độ lệch chuẩn của tập học, không bảo đảm dữ liệu trở thành phân phối Gaussian. Nếu áp dụng, các tham số biến đổi phải được học từ Train rồi dùng cho Validation/Test. Mô hình cây không nhất thiết cần bước chuẩn hóa này.',
50: 'Logarit có thể giảm chênh lệch về mức và phương sai với giá trị dương; sai phân mô tả thay đổi giữa các thời điểm. Các phép biến đổi không tự bảo đảm tính dừng và cần kiểm tra sau khi áp dụng. Pipeline hiện tại không dùng logarit, sai phân hoặc nội suy để tạo biến mục tiêu.',
52: 'Đặc trưng giúp mô hình hồi quy sử dụng lịch sử và thông tin lịch. Chất lượng dự báo cần được đánh giá trên giai đoạn chưa dùng để lựa chọn mô hình. Các nhóm đặc trưng thường gặp gồm:',
57: 'Cyclical Encoding (Mã hóa chu kỳ): Biến đổi giờ hoặc tháng bằng các thành phần sin và cos để biểu diễn tính vòng. Đây là một lựa chọn thiết kế; bộ 11 đặc trưng đã khóa của đề tài sử dụng giá trị lịch trực tiếp, không dùng mã hóa sin/cos.',
58: 'Đặc trưng nghiệp vụ có thể gồm thông tin thời tiết hoặc biến đo khác nếu thực sự có và biết tại thời điểm suy luận. Dataset và mô hình hiện tại không bổ sung nhiệt độ, ngày lễ hoặc dữ liệu từ hộ khác.',
60: 'Chia ngẫu nhiên có thể đưa quan sát tương lai vào Train khi mục tiêu là dự báo giai đoạn phía sau. Đánh giá theo thời gian giữ thứ tự giữa tập học, tập lựa chọn và tập kiểm thử, tránh mô phỏng sai thông tin sẵn có tại mốc dự báo.',
63: 'Time-based Split chia trục thời gian thành các đoạn liên tiếp. Trong đề tài, tỷ lệ 70%/15%/15% áp dụng trên toàn bộ trục giờ trước khi loại mẫu không hợp lệ. Train dùng để fit; Validation dùng để lựa chọn mô hình; Test đánh giá mô hình đã khóa. Số mẫu hợp lệ không nhất thiết giữ nguyên tỷ lệ của trục giờ.',
65: 'Walk-forward Validation đánh giá qua nhiều mốc hoặc nhiều đoạn nối tiếp. Cần phân biệt việc cập nhật quan sát đầu vào với việc fit lại mô hình tại mỗi vòng:',
69: 'Các phương pháp dự báo gồm mô hình thống kê, mô hình học máy và mạng nơ-ron. Những nhóm dưới đây là cơ sở tham khảo, không phải toàn bộ các mô hình đã được chạy trong đề tài:',
76: 'Random Forest Regressor kết hợp nhiều cây quyết định được huấn luyện trên các mẫu lấy lại và tập đặc trưng ngẫu nhiên. Cách kết hợp có thể giảm phương sai của một cây; mức sai số và hiện tượng quá khớp vẫn cần được đánh giá trên dữ liệu cụ thể.',
77: 'XGBoost và LightGBM là các thư viện cây tăng cường gradient. Các cây được bổ sung theo từng bước để cải thiện hàm mất mát. Chi phí huấn luyện phụ thuộc dữ liệu, cấu hình và môi trường; đề tài không triển khai hai thư viện này.',
79: 'LSTM sử dụng trạng thái ô nhớ và các cổng điều khiển để mô hình hóa quan hệ theo thời gian. Kiến trúc hỗ trợ học phụ thuộc dài hạn nhưng không bảo đảm loại bỏ mọi khó khăn tối ưu hoặc đạt sai số thấp hơn mô hình khác trên mọi dataset.',
80: 'GRU sử dụng các cổng reset và update để cập nhật trạng thái ẩn. Khác biệt về số tham số, thời gian huấn luyện và sai số so với LSTM phụ thuộc cấu hình và bài toán.',
81: 'Temporal Fusion Transformer kết hợp cơ chế attention với các thành phần xử lý thông tin chuỗi thời gian. Đây là hướng tham khảo về mô hình, chưa được huấn luyện hoặc so sánh trong thực nghiệm hiện tại.',
83: 'Sai số dự báo được xác định bằng cách so sánh giá trị ước lượng và giá trị thực tế trên cùng các mốc hợp lệ. Trong các công thức dưới đây, n là số mẫu, yᵢ là điện năng thực tế và ŷᵢ là điện năng dự báo:',
84: 'MAE (Mean Absolute Error) là trung bình độ lớn của sai số tuyệt đối. Đơn vị của MAE trùng với biến mục tiêu; trong đề tài là kWh.',
85: 'MSE (Mean Squared Error) là trung bình bình phương sai số, có đơn vị bình phương của biến mục tiêu. Giá trị sai số lớn được nhấn mạnh hơn so với MAE.',
86: 'RMSE (Root Mean Squared Error) là căn bậc hai của MSE, đưa kết quả về cùng đơn vị với biến mục tiêu.',
87: 'MAPE biểu diễn sai số theo tỷ lệ so với giá trị thực tế, nhưng không xác định khi giá trị thực tế bằng 0 và có thể nhạy với các giá trị gần 0. Đây không phải chỉ số được báo cáo cho mô hình hiện tại.',
88: 'sMAPE sử dụng cả độ lớn của dự báo và thực tế trong mẫu số; cần quy định trường hợp mẫu số bằng 0. Chỉ số này không được sử dụng để lựa chọn mô hình của đề tài.',
89: 'R² so sánh sai số bình phương với dự báo bằng trung bình của tập đánh giá; giá trị có thể âm và không phải phần trăm độ chính xác. Kết quả thực nghiệm sử dụng MAE và RMSE trên cùng tập mốc thời gian.',
91: 'Apache Flink là framework và bộ máy xử lý phân tán cho phép tính có trạng thái trên dữ liệu bounded và unbounded. Bounded có điểm kết thúc xác định; unbounded không có điểm kết thúc xác định trước. Yêu cầu độ trễ và khả năng mở rộng cần được đánh giá theo ứng dụng cụ thể.',
93: 'Batch Processing xử lý dữ liệu hữu hạn. Streaming Processing có thể xử lý dữ liệu hữu hạn hoặc không hữu hạn. Loại đầu vào và chế độ thực thi là hai khái niệm riêng; đề tài chọn SQL BATCH cho tệp UCI lịch sử.',
94: 'Một số khả năng của Flink',
95: 'Xử lý phân tán: Các tác vụ có thể được thực thi song song trên TaskManager. Đề tài chạy cục bộ với parallelism bằng 1, chưa đo hiệu năng cụm nhiều máy.',
96: 'Event Time và Watermark: Hỗ trợ xử lý theo dấu thời gian sự kiện trong các ứng dụng streaming được cấu hình tương ứng.',
97: 'Managed State: Cung cấp cơ chế quản lý trạng thái cho các phép tính liên tục. Trong hệ thống hiện tại, đặc trưng trễ và rolling được tạo bằng Python từ CSV theo giờ, không bằng DataStream State.',
98: 'Khôi phục trạng thái: Khi checkpoint được bật và các thành phần phù hợp, Flink có thể phục hồi trạng thái sau lỗi. Exactly-once của trạng thái không có nghĩa đoạn mã chỉ thực thi một lần; bảo đảm đầu-cuối còn phụ thuộc source và sink.',
102: 'TaskManager trực tiếp thực thi các subtask và trao đổi dữ liệu. Task Slot là đơn vị phân bổ tài nguyên logic bên trong TaskManager, không phải một máy hoặc một lõi CPU riêng. JobManager điều phối công việc; dữ liệu không cần đi qua JobManager để tính toán.',
105: 'Source tiếp nhận dữ liệu từ tệp hoặc hệ thống ngoài thông qua connector phù hợp. Connector có thể cần cài đặt và cấu hình riêng. Nguồn của đề tài là tệp TXT hữu hạn qua filesystem/CSV, không phải Kafka hoặc công tơ trực tiếp.',
106: 'Transformation thực hiện lọc, biến đổi hoặc tổng hợp. Trong DataStream API, map, filter và flatMap xử lý bản ghi; keyBy phân vùng logic theo khóa nhưng chưa thực hiện tổng hợp. Pipeline của đề tài sử dụng các biểu thức và phép GROUP BY trong Flink SQL.',
107: 'Sink xuất kết quả xử lý đến tệp hoặc hệ thống ngoài. Hệ thống hiện tại xuất CSV theo giờ; huấn luyện và suy luận HGB được thực hiện riêng bằng Python, không nằm trong Flink job.',
112: 'Event Time là dấu thời gian sự kiện theo dữ liệu nguồn, khác đồng hồ tại lúc xử lý. Khái niệm này phù hợp khi cần kết quả theo thời điểm phát sinh; tính đúng đắn vẫn phụ thuộc chất lượng timestamp và cấu hình xử lý.',
115: 'Watermark biểu diễn tiến độ Event Time dựa trên chiến lược của ứng dụng. Dấu mốc này hỗ trợ trigger quyết định thời điểm phát kết quả, không bảo đảm tuyệt đối mọi sự kiện cũ hơn đã đến. Bản ghi đến sau watermark vẫn có thể là dữ liệu trễ.',
117: 'Bounded-out-of-orderness Watermark ước lượng tiến độ từ timestamp đã quan sát và độ trễ cho phép. Đây là giả định của chiến lược, không phải giới hạn vật lý bảo đảm mọi bản ghi đều đến đúng hạn.',
118: 'Allowed Lateness cho phép một cửa sổ Event Time đã cấu hình tiếp nhận thêm bản ghi trễ trong khoảng gia hạn; việc phát lại kết quả phụ thuộc trigger và phép tính.',
119: 'Side Output có thể tách các bản ghi quá trễ khỏi kết quả cửa sổ nếu ứng dụng cấu hình luồng phụ. Job SQL BATCH của đề tài không khai báo watermark, allowed lateness hoặc side output.',
122: 'keyBy phân vùng logic DataStream theo khóa để các bản ghi cùng khóa được xử lý tại cùng instance song song phụ trách khóa đó. Không đồng nhất khóa với một Task Slot cố định hoặc xem keyBy là phép GROUP BY kèm tổng hợp.',
126: 'Sliding Window có kích thước W và bước trượt S. Các cửa sổ chồng lấn khi S nhỏ hơn W, nên một sự kiện có thể thuộc nhiều cửa sổ. Thống kê rolling của đề tài được tính trong Python, không triển khai qua DataStream Window.',
127: 'Session Window nhóm sự kiện theo khoảng không hoạt động; các phiên có thể được hợp nhất khi dữ liệu bổ sung nối chúng lại. Thời điểm phát kết quả phụ thuộc ngữ nghĩa thời gian và trigger, không chỉ đồng hồ thực tế.',
131: 'ReduceFunction và AggregateFunction hỗ trợ tổng hợp tăng dần, có thể giảm nhu cầu giữ toàn bộ bản ghi so với phép xử lý cửa sổ chỉ dùng ProcessWindowFunction.',
132: 'ProcessWindowFunction truy cập các phần tử của cửa sổ khi trigger kích hoạt và cung cấp ngữ cảnh cửa sổ. Nó có thể kết hợp với tổng hợp tăng dần; không mặc nhiên chỉ chạy đúng một lần khi cửa sổ kết thúc.',
134: 'Stateful Processing và cơ chế chịu lỗi là các khả năng của Flink cần được cấu hình phù hợp với ứng dụng:',
141: 'HashMapStateBackend giữ trạng thái làm việc trong heap của JVM. Dung lượng và hiệu năng chịu ảnh hưởng của bộ nhớ khả dụng, kích thước state và cấu hình.',
142: 'EmbeddedRocksDBStateBackend lưu trạng thái làm việc trong cơ sở dữ liệu nhúng trên đĩa cục bộ và sử dụng bộ nhớ cho bộ đệm. Lựa chọn backend tạo đánh đổi về truy cập lưu trữ và tài nguyên, không loại bỏ nhu cầu RAM.',
144: 'Checkpoint tạo snapshot nhất quán của trạng thái và vị trí đọc phù hợp khi được bật. Phục hồi còn phụ thuộc checkpoint thành công, nguồn có khả năng đọc lại và chính sách restart. Bảo đảm đầu-cuối cần sink tương thích; checkpoint có thể tạo thêm chi phí truyền, lưu và chờ đồng bộ.',
145: 'Savepoint thường được người dùng chủ động tạo cho thao tác có kế hoạch như dừng, nâng cấp hoặc rescaling. Khả năng phục hồi phụ thuộc tương thích trạng thái, định danh operator và cấu hình; không bảo đảm mọi thay đổi chương trình đều giữ được state.'
}

CH2_EXTRA = {
2: 'Các khái niệm trên theo cách tiếp cận chuỗi thời gian trong Forecasting: Principles and Practice của Hyndman và Athanasopoulos. Đề tài phân tích profile theo giờ, thứ và tháng; các chênh lệch quan sát được không tự chứng minh nguyên nhân hoặc một mô hình mùa vụ áp dụng cho mọi hộ.',
4: 'Chính sách thực nghiệm giữ nguyên những khoảng thiếu và không áp dụng forward fill, backward fill, nội suy, winsorization hoặc scaling. Điện năng giờ không đầy đủ nhận NULL; các mẫu dự báo thiếu lịch sử bắt buộc được loại theo quy tắc hợp lệ đã xác định trước khi huấn luyện.',
5: 'Bộ đặc trưng thực tế gồm năm lag ở 1, 2, 3, 24 và 168 giờ; hai trung bình của 3 và 24 giờ trước; bốn biến lịch của giờ mục tiêu. Các thống kê được tính trên trục giờ liên tục và dịch về quá khứ, không nối các dòng hợp lệ qua một khoảng mất dữ liệu.',
6: 'Thực nghiệm sử dụng một lần chia cố định và mô hình Train-only, không chạy các vòng fit lại kiểu expanding/sliding. Test được đánh giá một bước cuốn chiếu với quan sát quá khứ thực tế, nhưng tham số mô hình vẫn giữ nguyên.',
7: 'Hai baseline thực tế là Naive (dùng điện năng giờ trước) và Seasonal Naive 24 giờ (dùng cùng giờ ngày trước). Mô hình học máy được huấn luyện là HistGradientBoostingRegressor của scikit-learn. HGB xây dựng cây tăng cường trên các khoảng giá trị dạng histogram; đây không phải XGBoost, LightGBM, Random Forest hoặc mạng LSTM. Tài liệu scikit-learn 1.6.1 là nguồn mô tả thuật toán và tham số của HGB.',
11: 'Đối với dữ liệu hữu hạn hiện tại, timestamp nguồn được phân tích và làm tròn xuống mốc giờ trong SQL BATCH. Không có cơ chế watermark dùng để chốt cửa sổ trong job này; lý thuyết streaming không được xem là chức năng đã triển khai.',
12: 'Phép tổng hợp thực tế là GROUP BY FLOOR(event_time TO HOUR). Đây là gom các bản ghi theo khóa giờ trong SQL, không phải lời gọi keyBy hoặc TUMBLE trong DataStream API.',
13: 'Job hiện tại chạy SQL BATCH với chính sách restart không tự thử lại; không triển khai checkpoint streaming hoặc savepoint. Bằng chứng khôi phục ứng dụng liên quan tới khởi động lại dịch vụ và nạp artifact đã lưu, không chứng minh phục hồi state của một job streaming.'
}

CH2_14 = '''Apache Flink 2.3.0 được sử dụng ở chế độ SQL BATCH trên môi trường WSL2/Ubuntu với Java 17. Job đọc tệp dữ liệu UCI hữu hạn, kiểm tra giá trị và dấu thời gian, sau đó nhóm các bản ghi theo từng giờ để tổng hợp điện năng. Đầu ra được lưu thành CSV phục vụ các bước phân tích và dự báo.

Python được sử dụng cho xử lý dữ liệu sau tổng hợp và xây dựng mô hình. Pandas tổ chức chuỗi theo trục thời gian và tạo đặc trưng; NumPy hỗ trợ tính toán trên mảng số. HistGradientBoostingRegressor của scikit-learn được huấn luyện trên Train, lưu bằng joblib và nạp lại khi suy luận. Ứng dụng không huấn luyện lại mô hình khi người dùng mở hoặc chuyển tab.

Streamlit xây dựng giao diện Tổng quan, Phân tích và Dự báo; Plotly hiển thị biểu đồ tương tác. Dashboard đọc dữ liệu theo giờ và kết quả đánh giá đã lưu, sử dụng mô hình đã khóa để dự báo tại các mốc lịch sử hợp lệ. Huấn luyện và suy luận bằng Python là thành phần riêng, không được thực hiện bên trong job Flink.

Kiến trúc sử dụng nguồn dữ liệu lịch sử và các tệp kết quả trung gian. Kafka, PyFlink, InfluxDB, TimescaleDB, HDFS và Grafana không phải thành phần của ứng dụng hiện tại. Các cơ chế streaming được giới thiệu trong phần lý thuyết không đồng nghĩa đã triển khai nguồn công tơ trực tiếp.'''

CH3 = {
1: '''UCI Individual Household Electric Power Consumption ghi nhận phép đo điện của một hộ tại Sceaux, Pháp. Nguồn do Georges Hebrail và Alice Berard cung cấp trên UCI Machine Learning Repository. Tệp TXT trong ZIP được phân tách bằng dấu chấm phẩy; dòng đầu chứa tên chín thuộc tính, các dòng còn lại là quan sát theo phút.

Khoảng quan sát thực tế bắt đầu lúc 17:24 ngày 16/12/2006 và kết thúc lúc 21:02 ngày 26/11/2010, gồm 2.075.259 bản ghi. Đây là dữ liệu lịch sử của một hộ, không phải dữ liệu nhiều hộ hoặc dòng công tơ đang cập nhật. Trang UCI là nguồn mô tả thuộc tính; số lượng và chất lượng bản ghi được xác nhận bằng kiểm tra tệp gốc.''',
2: '''Hai cột Date và Time xác định thời điểm đo; bảy cột còn lại ghi các đại lượng điện. Tên cột, ý nghĩa và đơn vị được giữ tương ứng với mô tả UCI tại {T31}. Dữ liệu ngày có cả dạng ngày/tháng một hoặc hai chữ số, nên việc phân tích không chỉ dựa vào chuỗi mẫu của ngày đầu.

@TABLE:T31

Global_active_power là công suất tác dụng trung bình trong một phút, không phải điện năng theo giờ. Ba cột Sub_metering ghi điện năng theo Wh của ba nhóm khu vực/thiết bị, không đại diện cho ba hộ và không cho phép tách chính xác điện năng của từng thiết bị trong nhóm. Đơn vị Global_reactive_power được giữ theo mô tả kW của nguồn UCI; không tự đổi sang một đơn vị khác trong bộ dữ liệu.''',
3: '''Kiểm tra ban đầu đọc toàn bộ tệp theo luồng, xác nhận số dòng, số cột, dấu phân cách và kiểu giá trị. Date và Time được ghép thành timestamp; các trường đo được kiểm tra trước khi chuyển thành số. Cả dấu hỏi và giá trị rỗng đều được nhận diện là thiếu phép đo.

Chuỗi timestamp hợp lệ, không trùng và liên tiếp theo từng phút. Tuy vậy, thời điểm có bản ghi không đồng nghĩa có phép đo hợp lệ: 25.979 bản ghi thiếu giá trị đo vẫn tồn tại trên trục thời gian. Phân biệt này được giữ trong thống kê bản ghi và thống kê công suất hợp lệ.''',
4: '''Kết quả kiểm tra toàn bộ dữ liệu và kết quả theo giờ được tổng hợp tại {T32}. Kiểm tra timestamp không phát hiện thời điểm không hợp lệ hoặc trùng. Các khoảng thiếu phép đo có thể kéo dài nhiều ngày; khoảng liên tiếp dài nhất được ghi nhận là 7.226 phút.

@TABLE:T32

Phần điện năng còn lại được kiểm tra bằng cách lấy điện năng toàn phần theo phút trừ tổng ba nhóm đo phụ sau khi thống nhất đơn vị. Có 1.050 bản ghi cho kết quả âm. Những trường hợp này được ghi cờ chất lượng, không ép thành 0 và không kết luận tất cả chỉ do làm tròn. Biểu đồ nhóm đo phụ không trình bày phần còn lại như một phép đo thiết bị độc lập.''',
5: '''Quy trình không thay giá trị thiếu bằng 0, không tự nội suy khoảng mất phép đo và không loại các mức tiêu thụ cao chỉ vì khác trung bình. Trường số thiếu hoặc không chuyển đổi được không đóng góp vào số phép đo hợp lệ của giờ tương ứng.

Giờ không đầy đủ vẫn tồn tại trong bảng dữ liệu theo giờ. observed_energy_kwh lưu điện năng của những phút có phép đo, còn energy_kwh nhận NULL nếu không đủ điều kiện giờ hoàn chỉnh. Tập phân tích chỉ sử dụng đúng trường và phạm vi tương ứng; tập dự báo loại mẫu không có nhãn hoặc đặc trưng lịch sử bắt buộc. Quy tắc này không biến mất dữ liệu thành không sử dụng điện.''',
6: '''Date và Time được chuẩn hóa theo thứ tự ngày/tháng/năm của nguồn. SQL tách các thành phần ngày, bổ sung chữ số 0 khi cần và kiểm tra phép chuyển timestamp; kiểm tra ngày thực tế tránh chấp nhận một ngày chỉ đúng hình thức. Mốc giờ được xác định bằng cách làm tròn timestamp xuống đầu giờ.

Các timestamp được sử dụng theo lịch của nguồn, không gán một múi giờ đã được chứng minh. Quy ước timezone và giờ mùa hè chưa được xác minh; vì vậy báo cáo không gọi chuỗi là UTC hoặc khẳng định đã hiệu chỉnh DST. Đây là giới hạn khi diễn giải các mốc lịch sử, dù trục timestamp trong tệp liên tiếp từng phút.''',
7: '''Global_active_power biểu thị công suất tác dụng trung bình từng phút, đơn vị kW. Điện năng một phút bằng công suất nhân thời lượng 1/60 giờ. Với một giờ đủ 60 quan sát hợp lệ, energy_kwh bằng tổng công suất của các phút chia cho 60; điện năng nhóm đo phụ theo giờ bằng tổng Wh chia cho 1.000.

Quy tắc tại {T33} phân biệt kết quả ghi nhận một phần với điện năng giờ đầy đủ. Flink SQL BATCH nhóm theo FLOOR(event_time TO HOUR); không sử dụng keyBy, TUMBLE hoặc watermark để chốt cửa sổ.

@TABLE:T33

Kết quả tạo 34.589 khung giờ, gồm 34.085 giờ đầy đủ và 504 giờ không đầy đủ. Tập theo giờ và các cột chất lượng là đầu vào của bước phân tích và tạo đặc trưng. {F31} dành cho hình minh họa đầu ra tổng hợp theo giờ.

@FIG:F31''',
8: '''Thống kê trên dữ liệu giờ đã lưu được trình bày tại {T34}. Tổng điện năng quan sát gồm các phút hợp lệ của cả giờ đầy đủ và không đầy đủ. Ngược lại, giá trị trung bình, thấp nhất và cao nhất trong bảng chỉ sử dụng 34.085 giờ đầy đủ.

@TABLE:T34

Chênh lệch giữa tổng quan sát và tổng giờ đầy đủ phản ánh việc giữ riêng các phút của giờ thiếu. Độ phủ phút 98,7443% được tính trên 34.589 × 60 vị trí phút kỳ vọng, nên bao gồm cả phần không ghi nhận ở hai giờ biên; chỉ số này khác tỷ lệ bản ghi gốc có phép đo hợp lệ.''',
9: '''Các profile sử dụng điện năng của giờ đầy đủ, được nhóm theo giờ trong ngày, thứ trong tuần hoặc tháng. Trung bình theo giờ cao nhất tại 20 giờ, khoảng 1,8984 kWh; thấp nhất tại 4 giờ, khoảng 0,4439 kWh. Số quan sát của từng nhóm được giữ để tránh diễn giải các nhóm thiếu nhiều dữ liệu như cùng độ phủ.

Trung bình thứ Bảy khoảng 1,2465 kWh và Chủ nhật khoảng 1,2184 kWh; các ngày còn lại nằm trong khoảng 0,9806–1,0808 kWh. Khi gộp tháng qua các năm, tháng 12 có trung bình khoảng 1,4877 kWh và tháng 8 khoảng 0,5715 kWh. Những kết quả này mô tả hộ và giai đoạn quan sát, không chứng minh nguyên nhân do thời tiết, hành vi hoặc một quy luật áp dụng cho các hộ khác.''',
10: '''Ba nhóm đo phụ được phân tích trong cùng một hộ. Tổng điện năng ghi nhận của nhóm bếp là 2.299,135 kWh; nhóm giặt giũ là 2.661,031 kWh; nhóm bình nước nóng và điều hòa là 13.235,167 kWh trên toàn bộ thời gian nguồn. Đây là tổng các phép đo nhóm hợp lệ, không phải ước lượng phần điện năng đã mất.

Các nhóm không bao phủ toàn bộ mức sử dụng điện của hộ, nên không thể xem tổng ba nhóm là biến mục tiêu toàn nhà. Các cột số phép đo hợp lệ riêng theo nhóm hỗ trợ diễn giải độ phủ; không quy phần thiếu hoặc phần dư âm thành điện năng của một thiết bị khác.''',
11: '''Biểu đồ điện năng theo giờ đặt thời gian trên trục ngang và kWh trên trục dọc. Những giờ energy_kwh bằng NULL tạo khoảng trống, không nối qua bằng một giá trị thay thế. Profile theo giờ, thứ và tháng sử dụng những giờ đầy đủ; biểu đồ đo phụ hiển thị điện năng ghi nhận và thông tin độ phủ.

{F32} dành cho biểu đồ điện năng theo giờ. Dashboard cho phép thay đổi khoảng ngày; tiêu đề và chú thích cần được đọc cùng phạm vi lọc, thay vì sử dụng một tổng điện năng không ghi giai đoạn.

@FIG:F32''',
12: '''Tập sau xử lý gồm một dòng cho mỗi khung giờ, với hour_start, số bản ghi, số phút khác nhau, số công suất hợp lệ, cờ is_complete, observed_energy_kwh và energy_kwh. Các cột đo phụ giữ riêng số phép đo và điện năng ghi nhận; negative_residual_count ghi nhận số phút có phần dư âm.

Trục giờ liên tục là đầu vào tạo lag và rolling. Việc lọc mẫu dự báo diễn ra sau khi xây dựng đặc trưng trên trục này. Đầu ra dữ liệu giờ được lưu tách khỏi hồ sơ kiểm thử; mô hình và dashboard sử dụng artifact đã kiểm, không tự đọc lại hơn hai triệu bản ghi khi người dùng chuyển tab.''',
13: '''Dữ liệu gốc có timestamp liên tục nhưng tồn tại các khoảng mất giá trị đo. Phân biệt tính liên tục thời gian với độ đầy đủ phép đo là điều kiện để tổng hợp đúng đơn vị và tránh tạo nhãn sai cho mô hình. Chuỗi giờ giữ 504 khoảng không đầy đủ thay vì nén chúng khỏi trục.

Phân tích ghi nhận khác biệt mức tiêu thụ giữa các khung giờ, ngày và tháng; ba nhóm đo phụ cung cấp thông tin về các khu vực trong cùng hộ. Các thống kê không được sử dụng để suy ra khả năng dự báo các hộ khác. Tập đặc trưng và đánh giá mô hình cần giữ nguyên giới hạn dữ liệu lịch sử này.'''
}

CH4 = {
1: '''Bài toán là hồi quy dự báo điện năng tiêu thụ của một giờ kế tiếp cho một hộ gia đình. Gọi s là thời điểm bắt đầu khoảng giờ mục tiêu [s, s+1 giờ). Mốc phát dự báo là s; quan sát mới nhất được sử dụng là điện năng của khoảng [s−1 giờ, s).

Đánh giá theo một bước cuốn chiếu cho phép sử dụng quan sát thực tế của những giờ đã kết thúc, kể cả khi chúng thuộc đoạn Test. Mô hình không được học từ nhãn Test và không được fit lại tại từng mốc. Cách đánh giá này khác với dự báo nhiều tháng từ một mốc duy nhất mà không nhận thêm quan sát mới.''',
2: '''Biến mục tiêu là energy_kwh của khoảng giờ cần dự báo. Nhãn chỉ được xem là hợp lệ khi khoảng giờ có đủ phép đo công suất theo quy tắc chất lượng. observed_energy_kwh của một giờ thiếu không thay thế cho nhãn đầy đủ.

Giá trị mục tiêu có đơn vị kWh, không phải công suất kW hoặc tổng của ba nhóm đo phụ. Mỗi nhãn được gắn với giờ bắt đầu, mốc phát dự báo và giờ kết thúc để kiểm tra chiều thời gian giữa đầu vào và đầu ra.''',
3: '''Đầu vào được tạo từ chuỗi energy_kwh theo giờ và lịch của giờ mục tiêu. Mô hình không sử dụng điện năng tương lai, ba nhóm đo phụ, điện áp, cường độ dòng điện, thời tiết hoặc dữ liệu nhiều hộ làm feature.

Mẫu hợp lệ phải có nhãn đầy đủ cùng toàn bộ các lag và rolling bắt buộc. Calendar features của giờ mục tiêu được biết trước tại mốc dự báo, nên không phải giá trị đo tương lai. Mẫu không đủ lịch sử bị loại theo quy tắc cố định, không loại dựa trên việc dự báo dễ hay khó.''',
4: '''Bộ 11 đặc trưng và thứ tự sử dụng được trình bày tại {T41}. Năm lag tham chiếu chính xác mốc s−1, s−2, s−3, s−24 và s−168 giờ. Hai rolling lấy 3 hoặc 24 khoảng giờ ngay trước s, sau khi dịch chuỗi về quá khứ.

@TABLE:T41

Trung bình rolling chỉ hợp lệ khi toàn bộ các giờ trong cửa sổ quá khứ có điện năng đầy đủ. Lag tham chiếu theo timestamp, không theo vị trí của bảng đã bỏ dòng thiếu; một lag xa vẫn có thể hợp lệ nếu đúng giờ được tham chiếu có dữ liệu. Điều này không cho phép nén một khoảng thiếu để xem hai giờ ở hai phía của nó là liên tiếp.''',
5: '''Train, Validation và Test là ba đoạn nối tiếp theo thời gian. Tỷ lệ 70%/15%/15% được áp dụng trên trục 34.589 giờ trước khi lọc mẫu hợp lệ. Khoảng trục giờ và số mẫu sử dụng được đối chiếu tại {T42}.

@TABLE:T42

Tổng số mẫu hợp lệ là 31.830, gồm 22.513 Train, 4.727 Validation và 4.590 Test. Các giờ đầu chưa có đủ lag 168 giờ và những khoảng thiếu làm giảm số mẫu. Không chia ngẫu nhiên, không chuyển mẫu giữa các đoạn để cải thiện metric. Các feature của Validation/Test có thể tham chiếu quá khứ của đoạn trước nếu thông tin đó đã có tại mốc phát dự báo.''',
6: '''Naive dự báo bằng điện năng của giờ trước, tương ứng lag_1_kwh. Seasonal Naive 24 giờ dự báo bằng điện năng cùng giờ ngày trước, tương ứng lag_24_kwh. Hai phương pháp không cần fit mô hình học máy.

Cả hai baseline và HGB được đánh giá trên cùng mask mẫu hợp lệ để tránh so sánh các giai đoạn khác nhau. Baseline giúp xác định mức sai số đạt được chỉ từ những quy tắc lịch sử đơn giản, thay vì kết luận HGB có ích từ metric riêng của nó.''',
7: '''Mô hình học máy thực tế là HistGradientBoostingRegressor trong scikit-learn 1.6.1. HGB bổ sung các cây theo gradient của hàm mất mát và rời rạc hóa giá trị đặc trưng thành các bin. Cấu hình dùng loss squared_error, learning_rate 0,05, max_iter 200, max_leaf_nodes 15, min_samples_leaf 30, l2_regularization 1 và max_bins 255.

early_stopping được tắt và random_state bằng 42. Không có kết quả huấn luyện Random Forest, XGBoost, LightGBM, LSTM hoặc GRU trong thực nghiệm này. Các mô hình đó chỉ được đề cập ở cơ sở lý thuyết, không được đưa vào bảng so sánh như đã chạy.''',
8: '''HGB được fit bằng đúng 22.513 mẫu Train với 11 feature theo thứ tự cố định. Validation dùng để kiểm chứng và lựa chọn candidate; nhãn Validation không được dùng cho lần fit của candidate đã nghiệm thu. Môi trường Python 3.12.3 và scikit-learn 1.6.1 được giữ cho lưu/nạp.

Candidate được khóa trước khi đánh giá Test và không refit bằng Train cộng Validation. Dự báo cuối nhận giá trị lớn hơn hoặc bằng 0 theo quy tắc prediction_final = max(0, prediction_raw). Quy tắc này được xác định trước và áp dụng đồng nhất cho Validation, Test và suy luận, không thay đổi theo kết quả Test.''',
9: '''MAE và RMSE tính trên cùng các mốc mục tiêu hợp lệ, có đơn vị kWh. MAE biểu thị độ lớn sai số tuyệt đối trung bình; RMSE nhấn mạnh những sai số lớn hơn. Công thức native ở mục 2.8 xác định cách tính và ký hiệu; kết quả lưu được đối chiếu với phép tính độc lập trong kiểm thử mô hình.

{T43} trình bày kết quả Validation trên 4.727 mẫu. HGB có MAE 0,3694 kWh và RMSE 0,5306 kWh, thấp hơn hai baseline trên đoạn này. Đây là căn cứ lựa chọn candidate trước khi mở kết quả Test.

@TABLE:T43''',
10: '''{T44} trình bày kết quả Test cố định trên 4.590 mốc. HGB có MAE 0,3221 kWh và RMSE 0,4635 kWh; Naive lần lượt 0,3858 và 0,5845 kWh; Seasonal Naive 24 giờ lần lượt 0,5036 và 0,7526 kWh.

@TABLE:T44

HGB giữ mức sai số thấp hơn hai baseline trên đoạn Test này. MAE/RMSE Test thấp hơn Validation không tự chứng minh mô hình khái quát tốt hơn ở mọi giai đoạn, vì phân bố và mức tiêu thụ của hai đoạn có thể khác nhau. Không sử dụng kết quả Test để đổi model, feature, cấu hình hoặc mask mẫu.''',
11: '''Sai số được xác định trên từng mốc bằng chênh lệch dự báo và điện năng thực tế. MAE/RMSE là thống kê toàn tập, không có nghĩa mọi giờ đều có mức sai số bằng giá trị trung bình. Những giờ có mức tiêu thụ thay đổi mạnh vẫn có thể tạo sai số đáng kể.

Trong kết quả đã lưu, dự báo HGB thô âm là 0 trên cả Validation và Test. Vì vậy quy tắc chặn âm không làm thay đổi hai metric ở các đoạn này. Báo cáo không loại các mẫu sai số lớn để cải thiện kết quả và chưa thực hiện phân tích nguyên nhân sai số theo thiết bị hoặc thời tiết.''',
12: '''Biểu đồ trên tập Test đối chiếu đường điện năng thực tế và đường HGB theo cùng timestamp, như vị trí minh họa tại {F41}. Bộ lọc thời gian chỉ thay đổi phần kết quả được hiển thị; MAE/RMSE công bố vẫn là kết quả của toàn tập Test cố định.

@FIG:F41

Giá trị thực tế chỉ được hiển thị để đối chiếu sau suy luận, không đưa vào vector feature của giờ đó. Khi có khoảng không đủ điều kiện, giao diện không nội suy đường để tạo một dự báo chưa được mô hình sinh ra.''',
13: '''HGB được lựa chọn thông qua Validation trước khi đánh giá Test. Việc trình bày kết quả Test ở các mục đánh giá không thay đổi thứ tự lựa chọn trong thực nghiệm. Candidate Train-only tiếp tục được dùng và đóng gói thành model cuối, không tạo một lần fit mới sau khi biết Test.

Kết luận lựa chọn giới hạn ở một hộ, một horizon và các giai đoạn đã kiểm. Không suy ra HGB luôn tốt hơn các thuật toán khác, hoặc có thể dự báo điện năng của năm hiện tại từ dữ liệu kết thúc năm 2010.''',
14: '''Model được lưu bằng joblib kèm cấu hình, thứ tự feature, môi trường và quy tắc hậu xử lý. Artifact cuối đóng gói candidate đã kiểm, không refit. Kiểm thử lưu/nạp đối chiếu dự báo và khả năng tái lập của cùng mô hình.

Dashboard xác thực nguồn và model, tạo vector 11 feature tại mốc Test hợp lệ rồi dự báo một giờ. Mở hoặc chuyển tab không huấn luyện lại. Checksum và manifest phục vụ xác thực, không hiển thị mã dài cho người xem.'''
}

CH5 = {
1: '''Hệ thống cần đọc dữ liệu UCI lịch sử, kiểm tra bản ghi, tổng hợp điện năng theo giờ và cung cấp kết quả cho phân tích/dự báo. Dữ liệu thiếu phải được giữ như một trạng thái chất lượng, không biến thành điện năng bằng 0. Các chỉ số và dự báo cần thể hiện đơn vị, khoảng thời gian và đối tượng một hộ.

Yêu cầu giao diện là ba tab Tổng quan, Phân tích và Dự báo; cho phép lọc ngày, xem biểu đồ, thông tin bộ dữ liệu và suy luận tại mốc lịch sử hợp lệ. Yêu cầu vận hành gồm kiểm tra nguồn/model, tránh chiếm cổng của tiến trình khác và có thể khởi động lại dịch vụ do hệ thống quản lý. Tự khởi động sau coldboot và tiếp nhận công tơ trực tiếp không thuộc chức năng đã triển khai.''',
2: '''Kiến trúc gồm các thành phần nối tiếp: tệp UCI → Flink SQL BATCH → CSV điện năng theo giờ → tạo đặc trưng và huấn luyện bằng Python → model/kết quả đánh giá → dashboard. Flink trực tiếp thực hiện tổng hợp dữ liệu; dashboard không thay thế công việc này bằng một phép cộng lại dữ liệu phút khi hiển thị.

{T51} ghi công nghệ và vai trò thực tế. Flink cùng Python chạy trong Ubuntu trên WSL2; trình duyệt Windows truy cập ứng dụng qua localhost. Đây là cấu hình cục bộ, không phải triển khai phân tán nhiều máy hoặc dịch vụ đám mây.

@TABLE:T51''',
3: '''Tệp gốc được bảo toàn; job tạo đầu ra trong thư mục run riêng. Các bước tiếp theo đọc dữ liệu theo giờ đã được đối chiếu, xây dựng đặc trưng trên trục thời gian liên tục và chia Train/Validation/Test. Mô hình cuối được lưu riêng với dữ liệu và hồ sơ kiểm chứng.

Dashboard sử dụng artifact theo giờ, model và dự báo đánh giá đã lưu. Luồng phục vụ người dùng không yêu cầu chạy Flink hoặc huấn luyện lại mỗi lần thay bộ lọc. Mỗi tầng có điều kiện đầu vào riêng: dữ liệu giờ đúng schema, feature đúng thứ tự, model tương thích và mốc dự báo đủ lịch sử.''',
4: '''Flink SQL Client khai báo bảng nguồn qua filesystem connector và CSV format cho tệp TXT phân cách bằng dấu chấm phẩy. Dòng tiêu đề được bỏ qua; những trường ban đầu được đọc ở dạng có thể kiểm tra trước khi chuyển kiểu. Nguồn có điểm kết thúc, nên job được cấu hình BATCH.

Lượt xử lý toàn bộ nguồn đã kết thúc và có đầu ra kiểm chứng. Trạng thái job trong hồ sơ là bằng chứng lịch sử; không được dùng nó để khẳng định cluster hoặc job đang chạy tại mọi thời điểm. Chính sách lưu lịch sử REST có thể làm job cũ không còn tra được trong Web UI, dù artifact và hồ sơ vẫn tồn tại.''',
5: '''Các biểu thức SQL xử lý dấu hỏi, chuỗi rỗng và chuyển đổi trường số bằng phép cast an toàn. Giá trị không hợp lệ nhận NULL; số giá trị công suất hợp lệ được đếm độc lập với số bản ghi. Kiểm tra timestamp áp dụng cho dạng ngày/tháng một hoặc hai chữ số và đối chiếu ngày tồn tại.

Điện năng phần dư được tính sau khi quy đổi đơn vị để kiểm tra quan hệ giữa toàn phần và đo phụ. Phép tính giữ cờ âm, không sửa dữ liệu để làm mất ngoại lệ. Các thống kê chất lượng theo giờ được xuất cùng kết quả để tầng Python và UI không phải tự suy đoán độ đầy đủ.''',
6: '''Khóa nhóm là FLOOR(event_time TO HOUR), tức thời điểm đầu giờ của timestamp đã phân tích. GROUP BY tập hợp các phút thuộc cùng giờ để tính tổng, số bản ghi và số phép đo. Dataset chỉ có một hộ nên không bổ sung khóa hộ giả hoặc tạo bài toán nhiều hộ.

Phép nhóm SQL không được mô tả là lời gọi keyBy trong DataStream API. Parallelism thực tế bằng 1; khả năng phân tán của Flink là đặc tính công nghệ, còn hiệu năng nhiều worker chưa được đo trong cấu hình này.''',
7: '''Timestamp được tạo từ Date và Time theo lịch nguồn, chuẩn hóa phần ngày/tháng rồi kiểm tra chuyển đổi. event_time là tên trường trong SQL, không đồng nghĩa job đã khai báo thuộc tính thời gian streaming hoặc watermark. Giờ bắt đầu được làm tròn xuống để định vị khoảng [đầu giờ, đầu giờ + 1 giờ).

Job không cần chờ tiến độ watermark để tổng hợp một tệp hữu hạn. Không có allowed lateness hoặc side output cho dữ liệu đến trễ trong ứng dụng hiện tại. Múi giờ/DST của nguồn chưa được xác minh; không tự cộng hoặc trừ một độ lệch giờ cho các mốc dữ liệu.''',
8: '''SQL tổng hợp các phép đo trong mỗi khung giờ. Một giờ đầy đủ cần 60 bản ghi, 60 phút khác nhau và 60 công suất hợp lệ. Khi đủ điều kiện, energy_kwh là tổng kW chia cho 60; nếu thiếu, trường này nhận NULL và observed_energy_kwh giữ tổng ghi nhận một phần.

Các nhóm đo phụ được tổng hợp từ Wh sang kWh với số phép đo hợp lệ riêng. Số giờ đầy đủ và không đầy đủ được kiểm tra sau job. Thuật ngữ khung giờ trong báo cáo chỉ phạm vi tổng hợp SQL, không khẳng định sử dụng DataStream Window hoặc hàm TUMBLE.''',
9: '''Đầu ra gồm CSV theo giờ và hồ sơ run. Bảng giờ được tổ chức thành trục liên tục với 34.589 vị trí; các cột chất lượng và đo phụ giữ cùng hour_start. Đối chiếu độc lập kiểm tổng điện năng, số giờ và trạng thái NULL, không chỉ kiểm job đã FINISHED.

Artifact dữ liệu sản phẩm được xác thực bằng manifest và checksum ở tầng kỹ thuật. Cache/runtime Flink có thể bị dọn theo thời gian, không được xem là dữ liệu sản phẩm bất biến. Dashboard đọc CSV đã kiểm; thiếu hoặc sai nguồn phải được báo lỗi thay vì âm thầm dùng dữ liệu khác.''',
10: '''Tầng Python nạp model HGB đã lưu, kiểm schema và tạo feature tại mốc phát dự báo. Thứ tự 11 cột được giữ đúng cấu hình; vector không chứa nhãn của giờ mục tiêu. Dự báo thô được áp dụng quy tắc không âm trước khi hiển thị.

Ứng dụng có thể suy luận từ artifact khi Flink đã dừng, vì tổng hợp là một công đoạn trước đó. Điều này không làm mất vai trò của Flink: lineage ghi nhận dữ liệu giờ do job Flink tạo. Huấn luyện không diễn ra bên trong job hoặc khi mở dashboard.''',
11: '''Giao diện tổ chức ba tab chính, các thẻ chỉ số và biểu đồ. Bộ chọn khoảng ngày điều khiển phần dữ liệu được phân tích. Tổng quan hiển thị tổng điện năng ghi nhận, trung bình của giờ đầy đủ, giờ có mức tiêu thụ cao nhất và dự báo hợp lệ gần nhất trong khoảng chọn. {F51} dành cho màn hình Tổng quan.

@FIG:F51

Phần “Tìm hiểu bộ dữ liệu và cách AI dự báo” mặc định thu gọn. Khi mở, người xem có thông tin nguồn UCI, số dòng/cột, thời gian ghi nhận và hai bảng tách biệt: chín cột gốc và 11 đặc trưng được tạo sau xử lý. {F52} dành cho nội dung này; số hiệu được đặt trước các ảnh chức năng ở những mục tiếp theo.

@FIG:F52

Metadata như checksum, mã job và biểu thức chính sách nội bộ không được hiển thị trực tiếp trong phần giải thích cho người dùng, nhưng được giữ trong backend. Chú thích nêu rõ đây là dữ liệu lịch sử của một hộ và không phải dự báo điện năng hiện tại.''',
12: '''Phân tích hỗ trợ điện năng theo thời gian, profile theo giờ trong ngày, ngày trong tuần, tháng và ba nhóm đo phụ. Các thao tác và quy tắc dữ liệu của từng tab được đối chiếu tại {T52}.

@TABLE:T52

KPI tổng điện năng ghi nhận cộng các phút có phép đo trong khoảng chọn; không gọi đó là tổng đầy đủ khi độ phủ dưới 100%. Trung bình và cực trị sử dụng các giờ đầy đủ. Khi khoảng không có dữ liệu hoặc không có giờ đủ điều kiện, ứng dụng hiển thị trạng thái tương ứng thay vì chia cho 0, thay NULL bằng 0 hoặc dựng biểu đồ giả. {F53} dành cho tab Phân tích.

@FIG:F53''',
13: '''Tab Dự báo cung cấp các mốc thuộc Test có đủ feature, tổng cộng 4.590 mẫu trong nguồn đã khóa. Người dùng chọn một mốc lịch sử hợp lệ; ứng dụng hiển thị mốc phát dự báo, khoảng giờ mục tiêu và điện năng ước lượng theo kWh. Không cho nhập một ngày năm hiện tại rồi xem đó là suy luận đã được kiểm.

Vector đầu vào chỉ dùng lịch mục tiêu và điện năng quá khứ; nhãn thực tế của giờ đó được dùng riêng để đối chiếu. Những mốc không đủ lịch sử không được biến thành dự báo bằng cách điền số tùy ý. {F54} dành cho tab Dự báo.

@FIG:F54''',
14: '''Kết quả suy luận và điện năng thực tế được ghi nhãn riêng. Biểu đồ Test sử dụng dự báo đã lưu theo đúng mốc; các thẻ MAE và RMSE thể hiện kết quả trên 4.590 mẫu, không phải metric được tính lại cho một khoảng người dùng chọn. Mô hình đã khóa giữ MAE 0,3221 kWh và RMSE 0,4635 kWh.

Giá trị hiển thị được làm tròn để đọc, còn artifact lưu độ chính xác số gốc. Dự báo một bước tại mốc lịch sử không được trình bày như một lịch dự báo nhiều tháng. Cách hiển thị giúp tách kết quả mô hình, số thực tế và phạm vi đánh giá.''',
15: '''Phạm vi kiểm thử ở {T53} gồm chuỗi UCI → dữ liệu giờ Flink → feature → model → dashboard. Hồ sơ ứng dụng ghi nhận 126/126 kiểm đạt trong phạm vi I01, I02, I03 và I05; nhóm kiểm chức năng/vận hành có 119 kiểm, còn bảy kiểm liên quan gate bàn giao. Các kiểm này là bằng chứng tại thời điểm thực hiện, không bảo đảm runtime luôn hoạt động về sau.

@TABLE:T53

Với khoảng ví dụ 20–26/11/2010, dữ liệu nguồn chứa 166 khung giờ do kết thúc ngày 26 lúc 21:02; có 165 giờ đầy đủ. Tổng ghi nhận là 190,5417 kWh, trung bình giờ đầy đủ khoảng 1,1545 kWh và giờ cao nhất là 18 giờ ngày 20/11 với 5,6268 kWh. Phạm vi ngày không được mặc nhiên xem là đủ 168 giờ.

Lượt chỉnh phần giới thiệu dữ liệu có hồ sơ riêng 75 kiểm kỹ thuật và bảy kiểm trình duyệt ở 1366 × 768/1920 × 1080. Không cộng các lượt QA này thành số trường hợp độc lập không trùng.''',
16: '''Kiểm thử đã xác nhận các tab, bộ lọc, chỉ số, biểu đồ và suy luận trong phạm vi dữ liệu khóa. Các phép thử nguồn/model/cổng kiểm khả năng báo lỗi và tránh dừng tiến trình không thuộc hệ thống. Khởi động, dừng và phục hồi dịch vụ đã được kiểm ở môi trường cục bộ; coldboot Windows/WSL và autostart chưa được kiểm chứng hoặc triển khai.

I04 về kịch bản demo vẫn tạm hoãn, nên không kết luận toàn bộ Phase 4 đã hoàn tất. Kết quả kỹ thuật VERIFIED và việc người dùng nghiệm thu là hai trạng thái khác nhau. Báo cáo không có phép đo benchmark nhiều máy, kiểm tải production hoặc cam kết độ sẵn sàng dịch vụ.''',
17: '''Các giới hạn gồm một hộ lịch sử, khoảng mất phép đo, timezone/DST chưa xác minh và dự báo một bước. Ứng dụng không nhận dữ liệu công tơ mới, không tự cập nhật model và không dự báo nhiều bước khi không có quan sát bổ sung. Cấu hình Flink một máy chưa cho biết khả năng mở rộng theo số nguồn hoặc tài nguyên.

Hướng phát triển có thể gồm dữ liệu mới/nhiều hộ, đánh giá nhiều horizon và thiết kế nguồn cập nhật. Những thay đổi này cần xác định lại quy tắc chất lượng, feature, mô hình, cổng nghiệm thu và yêu cầu vận hành. Chúng là đề xuất, không phải chức năng đã triển khai của hệ thống hiện tại.'''
}

CONCLUSION = {
1: '''Báo cáo thực hiện phân tích dữ liệu tiêu thụ điện năng và dự báo điện năng của giờ kế tiếp từ bộ UCI Individual Household Electric Power Consumption. Apache Flink SQL BATCH xử lý 2.075.259 bản ghi theo phút và tổng hợp thành 34.589 khung giờ, trong đó 34.085 giờ có đủ phép đo hợp lệ. Các giờ không đầy đủ được đánh dấu để phân biệt điện năng ghi nhận với điện năng của một giờ hoàn chỉnh.

Từ dữ liệu theo giờ, quy trình xây dựng 11 đặc trưng lịch sử và lịch thời gian. HistGradientBoostingRegressor được huấn luyện trên 22.513 mẫu Train, lựa chọn thông qua Validation và giữ nguyên khi đánh giá trên 4.590 mẫu Test. MAE đạt 0,3221 kWh và RMSE đạt 0,4635 kWh, thấp hơn Naive và Seasonal Naive 24 giờ trên cùng tập kiểm tra.

Ứng dụng Streamlit gồm ba tab Tổng quan, Phân tích và Dự báo, sử dụng dữ liệu đã xử lý và mô hình đã lưu. Ứng dụng hỗ trợ xem mức tiêu thụ theo thời gian, ba nhóm đo phụ và dự báo tại các mốc lịch sử hợp lệ.''',
2: '''Dữ liệu chỉ ghi nhận một hộ gia đình tại Pháp trong giai đoạn 2006–2010, nên kết quả chưa đại diện cho các hộ khác hoặc nhu cầu điện hiện nay. Đánh giá sử dụng dự báo một bước cuốn chiếu: tại mỗi mốc, mô hình nhận các quan sát thực tế của những giờ trước để dự báo giờ kế tiếp. Đây không phải dự báo liên tục nhiều ngày hoặc nhiều tháng khi không có thêm quan sát.

Ứng dụng chưa kết nối với công tơ cập nhật trực tiếp và chưa được triển khai, kiểm chứng trong môi trường production nhiều máy. Các phép đo thiếu làm giảm số mẫu đủ điều kiện dự báo; quy ước múi giờ và thay đổi giờ mùa hè của nguồn chưa được xác minh.''',
3: '''Các hướng nghiên cứu tiếp theo gồm bổ sung dữ liệu của nhiều hộ và các giai đoạn mới, đánh giá khả năng dự báo nhiều bước, và xem xét nguồn dữ liệu cập nhật khi có điều kiện thu thập. Việc mở rộng cần xác định lại quy tắc chất lượng dữ liệu, điều kiện đánh giá và yêu cầu vận hành trước khi triển khai.'''
}

TABLES = {
'T31': (3, 1, 'Các thuộc tính của bộ dữ liệu UCI và đơn vị nguồn', ['Tên cột', 'Ý nghĩa', 'Đơn vị'], [5.2, 7.5, 2.3], [
['Date', 'Ngày ghi nhận', 'Ngày'], ['Time', 'Thời điểm đo trong ngày', 'Giờ:phút:giây'], ['Global_active_power', 'Công suất tác dụng trung bình từng phút', 'kW'], ['Global_reactive_power', 'Công suất phản kháng theo mô tả UCI', 'kW'], ['Voltage', 'Điện áp', 'V'], ['Global_intensity', 'Cường độ dòng điện', 'A'], ['Sub_metering_1', 'Điện năng nhóm khu vực bếp', 'Wh'], ['Sub_metering_2', 'Điện năng nhóm khu vực giặt giũ', 'Wh'], ['Sub_metering_3', 'Điện năng nhóm bình nước nóng và điều hòa', 'Wh']], 'Nguồn: UCI Machine Learning Repository; đối chiếu DATA_AUDIT của tệp gốc.'),
'T32': (3, 2, 'Kết quả kiểm tra chất lượng dữ liệu gốc và theo giờ', ['Chỉ tiêu', 'Kết quả', 'Phạm vi/ý nghĩa'], [6, 3, 6], [
['Bản ghi theo phút', '2.075.259', 'Toàn bộ tệp gốc'], ['Cột gốc', '9', 'Date, Time và bảy phép đo'], ['Bản ghi thiếu giá trị đo', '25.979', 'Không thay bằng 0'], ['Timestamp sai / trùng', '0 / 0', 'Kiểm toàn bộ timestamp'], ['Khoảng thiếu phép đo dài nhất', '7.226 phút', 'Các giá trị đo thiếu liên tiếp'], ['Khung giờ', '34.589', 'Trục thời gian sau tổng hợp'], ['Giờ đầy đủ / không đầy đủ', '34.085 / 504', 'Quy tắc đủ 60 phép đo'], ['Giờ không có công suất hợp lệ', '421', 'Thuộc nhóm giờ không đầy đủ'], ['Phút có phần điện năng dư âm', '1.050', 'Giữ cờ, không tự sửa']], 'Nguồn: audit toàn tệp và verification của lượt Flink toàn bộ dữ liệu.'),
'T33': (3, 3, 'Quy tắc tổng hợp và độ đầy đủ của khung giờ', ['Trường/quy tắc', 'Cách xác định'], [5.5, 9.5], [
['hour_start', 'FLOOR(event_time TO HOUR)'], ['record_count', 'Số bản ghi thuộc giờ'], ['distinct_minute_count', 'Số timestamp phút khác nhau'], ['valid_power_count', 'Số công suất tác dụng chuyển số hợp lệ'], ['is_complete', 'Ba số đếm trên đều bằng 60'], ['observed_energy_kwh', 'Tổng công suất hợp lệ (kW) chia 60'], ['energy_kwh', 'Bằng tổng ghi nhận khi đầy đủ; NULL nếu thiếu'], ['Điện năng nhóm đo phụ', 'Tổng giá trị Wh hợp lệ chia 1.000; giữ số phép đo riêng']], 'Nguồn: job.sql và schema hourly-grid.csv của lượt Flink đã kiểm.'),
'T34': (3, 4, 'Thống kê điện năng theo giờ trên toàn bộ giai đoạn', ['Chỉ tiêu', 'Giá trị', 'Phạm vi'], [5.6, 4.4, 5], [
['Tổng điện năng ghi nhận', '37.283,7477 kWh', 'Phút hợp lệ, kể cả giờ thiếu'], ['Tổng của giờ đầy đủ', '37.164,9650 kWh', '34.085 giờ đầy đủ'], ['Trung bình giờ đầy đủ', '1,0904 kWh', '34.085 giờ đầy đủ'], ['Giờ thấp nhất', '0,1240 kWh', '23/08/2008 21:00'], ['Giờ cao nhất', '6,5605 kWh', '23/11/2008 18:00'], ['Độ phủ phút theo trục giờ', '98,7443%', '34.589 × 60 vị trí phút']], 'Nguồn: thống kê đọc từ hourly-grid.csv đã khóa; không chạy lại Flink.'),
'T41': (4, 1, 'Bộ 11 đặc trưng đầu vào của mô hình dự báo', ['Đặc trưng', 'Ý nghĩa tại mốc s', 'Đơn vị/mã'], [5.2, 7.5, 2.3], [
['lag_1_kwh', 'Điện năng của giờ s−1', 'kWh'], ['lag_2_kwh', 'Điện năng của giờ s−2', 'kWh'], ['lag_3_kwh', 'Điện năng của giờ s−3', 'kWh'], ['lag_24_kwh', 'Điện năng cùng giờ ngày trước', 'kWh'], ['lag_168_kwh', 'Điện năng cùng giờ tuần trước', 'kWh'], ['rolling_mean_3_kwh', 'Trung bình ba giờ đầy đủ ngay trước s', 'kWh'], ['rolling_mean_24_kwh', 'Trung bình 24 giờ đầy đủ ngay trước s', 'kWh'], ['target_hour_of_day', 'Giờ của khoảng mục tiêu', '0–23'], ['target_day_of_week', 'Thứ của khoảng mục tiêu; thứ Hai = 0', '0–6'], ['target_month', 'Tháng của khoảng mục tiêu', '1–12'], ['target_is_weekend', 'Thứ Bảy/Chủ nhật = 1; ngày khác = 0', '0 hoặc 1']], 'Nguồn: feature-schema.json và prepare_baselines.py; thứ tự giữ đúng schema đã khóa.'),
'T42': (4, 2, 'Phân chia trục thời gian và số mẫu dự báo hợp lệ', ['Tập', 'Khoảng trục giờ (bao gồm hai đầu)', 'Giờ trục / mẫu hợp lệ'], [2.5, 8.5, 4], [
['Train', '16/12/2006 17:00 – 20/09/2009 12:00', '24.212 / 22.513'], ['Validation', '20/09/2009 13:00 – 24/04/2010 16:00', '5.188 / 4.727'], ['Test', '24/04/2010 17:00 – 26/11/2010 21:00', '5.189 / 4.590']], 'Nguồn: split-summary.json; Test hợp lệ cuối cùng bắt đầu 26/11/2010 20:00.'),
'T43': (4, 3, 'Kết quả Validation trên cùng 4.727 mẫu', ['Phương pháp', 'MAE (kWh)', 'RMSE (kWh)'], [7, 4, 4], [
['Naive', '0,4593', '0,6828'], ['Seasonal Naive 24 giờ', '0,6597', '0,9503'], ['HGB Train-only', '0,3694', '0,5306']], 'Nguồn: metric Validation đã khóa của baseline và candidate HGB; làm tròn bốn chữ số.'),
'T44': (4, 4, 'Kết quả Test trên cùng 4.590 mẫu', ['Phương pháp', 'MAE (kWh)', 'RMSE (kWh)'], [7, 4, 4], [
['Naive', '0,3858', '0,5845'], ['Seasonal Naive 24 giờ', '0,5036', '0,7526'], ['HGB Train-only', '0,3221', '0,4635']], 'Nguồn: metrics-test.json đã khóa; không fit lại sau khi xem Test.'),
'T51': (5, 1, 'Thành phần và môi trường công nghệ thực tế', ['Thành phần', 'Phiên bản/môi trường', 'Vai trò'], [4.6, 4.8, 5.6], [
['Apache Flink', '2.3.0; SQL BATCH', 'Đọc tệp, kiểm tra, tổng hợp theo giờ'], ['Java / Linux', 'Java 17; Ubuntu 24.04 trên WSL2', 'Môi trường thực thi Flink'], ['Python', '3.12.3', 'Tạo feature, học và suy luận'], ['Pandas / NumPy', '2.2.3 / 2.2.6', 'Trục thời gian và tính toán mảng'], ['scikit-learn', '1.6.1', 'HistGradientBoostingRegressor'], ['Streamlit / Plotly', '1.50.0 / 6.3.0', 'Giao diện ba tab và biểu đồ']], 'Nguồn: môi trường và requirements đã kiểm tại hồ sơ triển khai; không phải phiên bản mới nhất chung.'),
'T52': (5, 2, 'Chức năng và quy tắc dữ liệu của dashboard', ['Tab/khu vực', 'Dữ liệu/chức năng', 'Quy tắc/giới hạn'], [3.2, 6, 5.8], [
['Tổng quan', 'KPI, điện năng giờ, đo phụ, dự báo gần nhất', 'Tổng ghi nhận kèm độ phủ; trung bình/cực trị dùng giờ đầy đủ'], ['Phân tích', 'Profile giờ, thứ, tháng; chất lượng và đo phụ', 'Không thay NULL bằng 0; ghi phạm vi lọc'], ['Dự báo', 'Chọn mốc, suy luận HGB, đối chiếu Test', 'Mốc Test hợp lệ; model cố định; metric toàn Test'], ['Giới thiệu dữ liệu', 'Nguồn UCI, bảng 9 cột và 11 feature', 'Tách dữ liệu gốc khỏi đặc trưng được tạo']], 'Nguồn: dashboard/app.py, data_service.py, predictor.py và QA trình duyệt đã kiểm.'),
'T53': (5, 3, 'Phạm vi kiểm thử ứng dụng trong hồ sơ Phase 4', ['Nhóm kiểm', 'Kết quả', 'Nội dung'], [4.4, 2.7, 7.9], [
['Lineage / integration', '17/17', 'Đối chiếu nguồn và artifact nối các tầng'], ['Backend / AppTest', '67/67', 'KPI, lọc, NULL, suy luận, lỗi nguồn/model'], ['Vận hành Linux', '20/20', 'Khởi động/dừng/phục hồi; ownership/cổng'], ['Truy cập Windows', '4/4', 'Localhost ứng dụng và Flink'], ['Trình duyệt', '11/11', 'Ba tab, các tương tác và ảnh QA'], ['Gate bàn giao', '7/7', 'Hồ sơ và kiểm bảo toàn trong lượt bàn giao']], 'Nguồn: checklist/review/verification Phase4-app; snapshot kiểm, không bao gồm I04 hoặc coldboot.')
}

FIGURES = {
'F31': (3, 1, 'Đầu ra điện năng và chất lượng dữ liệu theo giờ', '3.7', 7.0, 'IMG02', 'Ảnh bảng dữ liệu giờ của lượt Flink; giữ energy_kwh NULL và cột chất lượng.'),
'F32': (3, 2, 'Điện năng tiêu thụ theo giờ trong khoảng thời gian lựa chọn', '3.11', 8.0, 'IMG03', 'Biểu đồ điện năng thật từ dashboard; ghi khoảng ngày và khoảng trống giờ thiếu.'),
'F41': (4, 1, 'Đối chiếu điện năng thực tế và dự báo HGB trên tập Test', '4.12', 8.0, 'IMG04', 'Biểu đồ thực tế/dự báo của Test đã lưu; không dựng dữ liệu minh họa.'),
'F51': (5, 1, 'Giao diện Tổng quan của ứng dụng', '5.11', 8.2, 'IMG05', 'Ảnh Tổng quan ứng dụng đã kiểm; phạm vi ngày và KPI cùng nguồn.'),
'F52': (5, 2, 'Phần giới thiệu bộ dữ liệu và đặc trưng dự báo', '5.11', 8.2, 'IMG08', 'Expander mở với bảng cột gốc/feature; không chèn trước Hình 5.1.'),
'F53': (5, 3, 'Giao diện Phân tích dữ liệu tiêu thụ điện năng', '5.12', 8.2, 'IMG06', 'Ảnh tab Phân tích thật, đơn vị và bộ lọc rõ.'),
'F54': (5, 4, 'Giao diện Dự báo điện năng của giờ kế tiếp', '5.13', 8.2, 'IMG07', 'Ảnh tab Dự báo ở mốc Test hợp lệ, mục tiêu và thực tế phân biệt.')
}

NEW_REFERENCES = [
('scikit-learn developers (n.d.). HistGradientBoostingRegressor. scikit-learn 1.6.1 documentation.', 'https://scikit-learn.org/1.6/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html'),
('scikit-learn developers (n.d.). Lagged features for time series forecasting. scikit-learn 1.6.1 examples.', 'https://scikit-learn.org/1.6/auto_examples/applications/plot_time_series_lagged_features.html'),
('Apache Software Foundation (n.d.). Execution Mode (Batch/Streaming). Apache Flink 2.3 documentation.', 'https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/execution_mode/'),
('Apache Software Foundation (n.d.). Group Aggregation. Apache Flink 2.3 SQL documentation.', 'https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/group-agg/'),
('Apache Software Foundation (n.d.). Windows. Apache Flink 2.3 DataStream documentation.', 'https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/operators/windows/')
]
