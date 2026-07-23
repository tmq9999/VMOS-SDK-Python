# VMOS SDK — Tài liệu API (Tiếng Việt)

> Được sinh tự động từ [tài liệu chính thức VMOS Cloud OpenAPI](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Mô tả tham số giữ nguyên tiếng Anh theo tài liệu gốc.

Mỗi namespace bên dưới là một thuộc tính của `VMOSClient` / `AsyncVMOSClient` (ví dụ `client.instance`). Dùng async giống hệt — chỉ cần `await` cùng phương thức.

| Module | Số endpoint | Mô tả |
|---|---|---|
| [`client.apps`](apps.md) | 10 | Cài/gỡ, khởi chạy/dừng/khởi động lại ứng dụng, liệt kê ứng dụng, giữ ứng dụng chạy nền và ẩn ứng dụng. |
| [`client.automation`](automation.md) | 25 | Kịch bản RPA, điều phối & lập lịch tác vụ, ma trận tài khoản, webview, livestream không người trực. |
| [`client.dynamic_proxy`](dynamic_proxy.md) | 13 | Khu vực proxy động, gói, đơn hàng, số dư lưu lượng, cấu hình proxy cho từng máy. |
| [`client.email`](email.md) | 5 | Loại email & tồn kho, đơn mua, lấy mã xác minh. |
| [`client.instance`](instance.md) | 50 | Khởi động lại/reset, thuộc tính, SIM/GPS/WiFi, lệnh ADB & shell, chụp màn hình, xem trước, nâng cấp image, đổi máy một chạm, bật/tắt root, công cụ mạng, chèn media. |
| [`client.phone`](phone.md) | 21 | Gói dịch vụ, đơn hàng, gia hạn, mã kích hoạt, ủy quyền/chuyển giao, sao lưu, chia sẻ, thay thế thiết bị. |
| [`client.static_proxy`](static_proxy.md) | 7 | Gói IP dân cư tĩnh, đơn hàng, tạo/gia hạn/quản lý proxy. |
| [`client.storage`](storage.md) | 11 | Gói lưu trữ, sao lưu cloud space, tải lên/truy vấn/xóa file, gia hạn lưu trữ. |
| [`client.tasks`](tasks.md) | 4 | Truy vấn trạng thái & chi tiết các tác vụ bất đồng bộ (thao tác instance, đẩy file). |
| [`client.token`](token.md) | 2 | Cấp & xóa token STS tạm thời cho SDK phía client. |
| [`client.touch`](touch.md) | 4 | Quỹ đạo chạm/vuốt/nhấn giữ giống người thật và cảm ứng đa điểm mức thấp. |

## Hướng dẫn chuyên đề

- [**Device Profile Framework — thiết kế chính thức**](device-profile-framework-vi.md)
- [Thiết bị thật — thuộc tính đổi được](thiet-bi-that-properties.md)
- [Toolkit spoof thiết bị (reseller)](toolkit-spoof-thiet-bi.md)
- [Đánh giá module Xposed/LSPosed spoof](xposed-spoof-modules-vi.md)
- [Hook XPose riêng — IMEI/IMSI/ICCID/ANDROID_ID (`apmt`)](xpose-custom-hook-vi.md)


**Total: 152 endpoints / 11 namespaces.**

Xem thêm: [../en/README.md](../en/README.md) — English documentation.
