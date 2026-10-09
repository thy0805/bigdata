# Script thuyết trình Apache Flink



HÂU
## Slide 1. Apache Flink

Em xin chào thầy và các bạn. Nhóm em xin trình bày chủ đề Apache Flink

## Slide 2. Nội dung trình bày

Bài trình bày gồm bốn phần chính: tổng quan về Apache Flink, kiến trúc và các thành phần, cơ chế xử lý dữ liệu, cuối cùng là phần đánh giá và ứng dụng.

## Slide 3. 1. Tổng quan

Dữ liệu ngày càng có khối lượng lớn, phát sinh nhanh và đến từ nhiều nguồn như giao dịch, nhật ký ứng dụng hay cảm biến. Khi quy mô dữ liệu vượt khả năng xử lý của một máy, công việc cần được phân chia trên nhiều máy. Đồng thời, với những bài toán như phát hiện giao dịch bất thường, kết quả còn cần được cập nhật liên tục.
Về nguồn gốc, Apache Flink bắt đầu từ dự án nghiên cứu Stratosphere vào năm 2009, được phát triển tại Đại học Kỹ thuật Berlin cùng một số đơn vị nghiên cứu khác, với mục tiêu xây dựng nền tảng xử lý và phân tích dữ liệu lớn theo hướng phân tán.
Tháng 4 năm 2014, Stratosphere gia nhập Apache Incubator và sau đó được đổi tên thành Flink. Đến tháng 12 năm 2014, Flink trở thành một dự án cấp cao, hay Top-Level Project, của Apache Software Foundation.
Trong quá trình phát triển, Flink tập trung mạnh vào xử lý dữ liệu liên tục và stateful processing, tức hệ thống có thể ghi nhớ trạng thái qua nhiều sự kiện. Ví dụ, khi tính tổng giao dịch của từng tài khoản, hệ thống phải lưu tổng hiện tại để tiếp tục cập nhật khi giao dịch mới xuất hiện

## Slide 4. Apache Flink

Apache Flink là một framework và bộ máy xử lý phân tán dành cho các phép tính có trạng thái trên dữ liệu bounded và unbounded.

Có trạng thái nghĩa là phép tính có thể ghi nhớ thông tin qua nhiều sự kiện. Ví dụ, để tính tổng giao dịch của từng tài khoản, hệ thống phải giữ lại tổng hiện tại rồi cập nhật khi có giao dịch mới.

Trong hệ sinh thái Big Data, Flink nằm ở lớp xử lý. Dữ liệu đi từ nguồn vào Flink, được lọc, biến đổi hoặc tổng hợp, sau đó chuyển tới hệ thống lưu trữ hoặc ứng dụng phía sau.

Bounded là dữ liệu có điểm kết thúc xác định. Unbounded là dữ liệu không có điểm kết thúc xác định trước.

Cần phân biệt loại dữ liệu với cách xử lý: streaming có thể xử lý cả bounded và unbounded, còn batch chỉ dành cho đầu vào bounded.

## Slide 5. 2. Kiến trúc

Sơ đồ này minh họa cách các thành phần chính của Flink phối hợp với nhau.

Đầu tiên là Flink Client, hỗ trợ chuẩn bị và gửi job lên cụm. Sau khi job được gửi, JobManager chịu trách nhiệm điều phối quá trình thực thi.

Bên trong JobManager có ba thành phần chính. Dispatcher tiếp nhận yêu cầu nộp job. ResourceManager quản lý việc cấp phát tài nguyên. JobMaster quản lý quá trình thực thi của một job cụ thể.

Phần trực tiếp xử lý dữ liệu là các TaskManager. Chúng thực hiện công việc được giao và trao đổi dữ liệu với nhau. Dữ liệu xử lý không cần đi qua JobManager để thực hiện phép tính.

Bên trong mỗi TaskManager có các Task Slot, được dùng làm đơn vị phân bổ tài nguyên. Slot là đơn vị logic, không phải một máy riêng và cũng không tương đương tuyệt đối với một lõi CPU.

## Slide 6. Từ chương trình đến quá trình thực thi

Flink biểu diễn công việc dưới dạng JobGraph, mô tả các thành phần xử lý và quan hệ truyền dữ liệu giữa chúng.

Từ đó hệ thống xây dựng ExecutionGraph, là biểu diễn đã được song song hóa để phục vụ quá trình thực thi.

Một Task là đơn vị công việc, còn Subtask là một phiên bản thực thi song song của Task. Ví dụ, Task có parallelism bằng hai thì sẽ có hai Subtask tương ứng.

Flink còn có Operator Chaining, cho phép ghép các operator phù hợp vào cùng một Task, và Slot Sharing, cho phép các phần công việc phù hợp chia sẻ tài nguyên trong cùng job.



Khoi
## Slide 7. 3. Cơ chế xử lý

Flink cung cấp DataStream API và Table API kết hợp SQL.

DataStream API phù hợp khi cần mô tả chi tiết logic xử lý sự kiện. Table API và SQL sử dụng mô hình quan hệ và cách khai báo ở mức cao hơn.

Với DataStream, Map biến đổi bản ghi, Filter giữ hoặc loại bản ghi theo điều kiện, còn FlatMap có thể tạo ra không, một hoặc nhiều đầu ra từ một bản ghi.

KeyBy đưa các bản ghi cùng khóa về cùng một phân vùng logic. Bản thân KeyBy chưa thực hiện tổng hợp. Các phép như Reduce mới thực hiện bước đó.

Có thể hình dung luồng cơ bản là: dữ liệu vào, biến đổi, phân vùng theo khóa rồi thực hiện tổng hợp.

## Slide 8. Thời gian trong Apache Flink

Trong xử lý luồng, thời điểm sự kiện xảy ra có thể khác thời điểm dữ liệu được tiếp nhận và xử lý.

Ví dụ một phép đo xảy ra lúc 10 giờ, đi vào hệ thống lúc 10 giờ 02, và được xử lý lúc 10 giờ 03. Ba mốc này lần lượt minh họa cho Event Time, Ingestion Time và Processing Time.

Event Time dựa vào timestamp của sự kiện. Processing Time dựa vào đồng hồ của máy đang xử lý. Khi cần thống kê theo đúng thời điểm sự kiện phát sinh, Event Time giúp giảm sự phụ thuộc vào độ trễ truyền dữ liệu.

Tuy nhiên, dữ liệu có thể đến không đúng thứ tự. Watermark biểu diễn tiến độ Event Time và hỗ trợ xác định khi nào có thể phát kết quả. Watermark không đảm bảo tuyệt đối rằng mọi sự kiện cũ hơn đã đến hết.

Với cửa sổ Event Time, Allowed Lateness cho phép cửa sổ tiếp tục nhận thêm bản ghi trễ trong giới hạn cấu hình. Bản ghi quá trễ có thể được chuyển sang Side Output nếu ứng dụng cấu hình luồng riêng.

## Slide 9. Window và xử lý dữ liệu theo thời gian

Window dùng để chia luồng dữ liệu thành các phạm vi hữu hạn để thực hiện phép tính.

Tumbling Window có kích thước cố định và không chồng lấn. Ví dụ có thể chia dữ liệu thành từng khoảng 5 phút liên tiếp.

Sliding Window có kích thước và chu kỳ trượt. Khi chu kỳ trượt nhỏ hơn kích thước cửa sổ thì các cửa sổ chồng lấn, nên một sự kiện có thể thuộc nhiều cửa sổ.

Còn Session Window nhóm các sự kiện theo phiên dựa trên khoảng không hoạt động, thay vì dùng các mốc cố định.

Khi sử dụng Event Time, thời điểm phát kết quả của cửa sổ còn phụ thuộc vào watermark và cơ chế kích hoạt, chứ không chỉ dựa trên đồng hồ thực tế.

## Slide 10. State và khả năng chịu lỗi

State là thông tin mà phép tính duy trì qua nhiều sự kiện, ví dụ một bộ đếm hoặc tổng giá trị đang tích lũy.

Flink hỗ trợ Keyed State, gắn với từng khóa của KeyedStream, và Operator State, gắn với từng instance song song của operator.

Checkpoint ghi lại ảnh chụp nhất quán của trạng thái cùng vị trí đọc dữ liệu phù hợp. Khi checkpoint được bật và cấu hình phục hồi phù hợp, Flink có thể khôi phục trạng thái từ checkpoint sau sự cố.

Trong khi đó, Savepoint thường được dùng cho các thao tác có kế hoạch như dừng, nâng cấp hoặc thay đổi mức song song.

Flink cũng phân biệt ba mức bảo đảm. At-most-once có thể mất bản ghi. At-least-once có thể xử lý lặp. Exactly-once nghĩa là kết quả trạng thái tương đương việc mỗi sự kiện có tác động một lần, mặc dù bản ghi vẫn có thể được xử lý lại trong lúc phục hồi.

Nếu xét toàn bộ từ đầu vào đến đầu ra, mức bảo đảm còn phụ thuộc khả năng của Source, Sink và Connector, không chỉ riêng checkpoint.


phat
## Slide 11. 4. Đánh giá & ứng dụng

Từ các cơ chế vừa trình bày, Flink có bốn ưu điểm chính.

Thứ nhất, Flink hỗ trợ cả streaming và batch. Thứ hai, hệ thống có thể duy trì trạng thái cho các phép tính liên tục. Thứ ba, Event Time và các cơ chế xử lý dữ liệu trễ giúp ứng dụng làm việc với dữ liệu đến không đúng thứ tự. Cuối cùng, checkpoint tạo cơ sở để khôi phục trạng thái khi xảy ra sự cố.

Tuy nhiên, những khả năng này cũng tạo ra các đánh đổi.

Tài nguyên của TaskManager phải được cấu hình phù hợp với workload. Checkpoint tạo thêm chi phí ghi, truyền và lưu snapshot. Nếu checkpoint quá thưa thì khi xảy ra lỗi có thể phải xử lý lại nhiều dữ liệu hơn.

Ngoài ra, khi state lớn, hệ thống cần nhiều bộ nhớ hoặc lưu trữ hơn và phải lựa chọn state backend phù hợp. Vì vậy hiệu năng thực tế cần được đánh giá trên bài toán và cấu hình cụ thể.

## Slide 12. So sánh các hệ thống xử lý dữ liệu

Nếu so với Hadoop MapReduce, MapReduce chủ yếu thực hiện các job batch trên tập dữ liệu đầu vào. Khi một task thất bại, framework có thể tổ chức thực thi lại task.

Flink ngoài batch còn hỗ trợ streaming, Event Time, Watermark, managed state và checkpoint. Các cơ chế này phù hợp với các ứng dụng cần xử lý sự kiện có trạng thái.

Còn Spark Structured Streaming được xây dựng trên Spark SQL và sử dụng DataFrame, Dataset cùng SQL. Chế độ mặc định là micro-batch, tức dữ liệu được xử lý qua các lô nhỏ liên tiếp. Spark cũng hỗ trợ Event Time, watermark và các phép tính có trạng thái, nên những khả năng này không chỉ có ở Flink.

Vì vậy không thể chỉ nhìn vào kiến trúc rồi kết luận Flink luôn nhanh hơn Spark hay Hadoop. Việc lựa chọn phải dựa trên loại dữ liệu, yêu cầu thời gian phản hồi, state, API và hệ sinh thái đang sử dụng.

## Slide 13. Ứng dụng của Apache Flink

Apache Flink có ba nhóm ứng dụng chính.

Nhóm thứ nhất là Event-driven Applications, trong đó dữ liệu mới kết hợp với trạng thái đã lưu để tạo phản ứng như giám sát hoạt động, phát hiện bất thường hoặc cảnh báo.

Nhóm thứ hai là Data Analytics, dùng Flink để cập nhật các chỉ số trên dữ liệu luồng hoặc tổng hợp dữ liệu batch.

Nhóm thứ ba là Data Pipelines, trong đó Flink thực hiện các bước ETL như chuẩn hóa, biến đổi rồi chuyển dữ liệu giữa các hệ thống.

Một trường hợp thực tế được Apache công bố là Capital One, sử dụng Flink cho giám sát hoạt động và cảnh báo theo thời gian thực.

Ngoài ba nhóm trên, báo cáo sử dụng dữ liệu điện năng như một lĩnh vực minh họa. Với dữ liệu công tơ, Flink có thể tổng hợp mức tiêu thụ theo từng hộ và theo thời gian.

Bộ London Smart Meter trong báo cáo là dữ liệu lịch sử, vì vậy đây chỉ là ví dụ minh họa khả năng áp dụng Flink, chưa phải hệ thống công tơ thời gian thực mà nhóm đã triển khai.

## Slide 14. Cảm ơn

Phần trình bày của nhóm em đến đây là kết thúc. Nhóm em xin cảm ơn thầy và các bạn đã lắng nghe.


