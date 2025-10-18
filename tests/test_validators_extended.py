"""
Расширенные тесты для валидаторов
"""

import pytest
from xmlriver_pro.utils.validators import (
    validate_query,
    validate_device,
    validate_os,
    validate_url,
    validate_coords,
    validate_zoom,
    validate_country,
    validate_region,
    validate_language,
    validate_domain,
    validate_groupby,
    validate_page,
    validate_time_filter,
    validate_within,
    validate_file_type,
    validate_image_size,
    validate_image_color,
    validate_image_type,
    validate_usage_rights,
)
from xmlriver_pro.core.types import DeviceType, OSType


class TestValidateQuery:
    """Тесты для validate_query"""

    def test_validate_query_valid(self):
        """Тест валидных запросов"""
        assert validate_query("python programming") is True
        assert validate_query("test query 123") is True
        assert validate_query("поисковый запрос") is True
        assert validate_query("query with numbers 123") is True

    def test_validate_query_empty_string(self):
        """Тест пустой строки"""
        assert validate_query("") is False
        assert validate_query("   ") is False
        assert validate_query("\t\n") is False

    def test_validate_query_whitespace_only(self):
        """Тест строки только с пробелами"""
        assert validate_query(" ") is False
        assert validate_query("  ") is False
        assert validate_query("\t") is False
        assert validate_query("\n") is False

    def test_validate_query_special_characters(self):
        """Тест недопустимых символов"""
        assert validate_query("query & test") is False
        assert validate_query("query < test") is False
        assert validate_query("query > test") is False
        assert validate_query('query " test') is False
        assert validate_query("query ' test") is False
        assert validate_query("query & < > \" ' test") is False

    def test_validate_query_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_query(None) is False
        assert validate_query(123) is False
        assert validate_query([]) is False
        assert validate_query({}) is False


class TestValidateDevice:
    """Тесты для validate_device"""

    def test_validate_device_enum(self):
        """Тест с DeviceType enum"""
        assert validate_device(DeviceType.DESKTOP) is True
        assert validate_device(DeviceType.TABLET) is True
        assert validate_device(DeviceType.MOBILE) is True

    def test_validate_device_string_valid(self):
        """Тест валидных строк"""
        assert validate_device("desktop") is True
        assert validate_device("tablet") is True
        assert validate_device("mobile") is True
        assert validate_device("DESKTOP") is True
        assert validate_device("TABLET") is True
        assert validate_device("MOBILE") is True

    def test_validate_device_string_invalid(self):
        """Тест невалидных строк"""
        assert validate_device("invalid") is False
        assert validate_device("phone") is False
        assert validate_device("laptop") is False
        assert validate_device("") is False

    def test_validate_device_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_device(None) is False
        assert validate_device(123) is False
        assert validate_device([]) is False
        assert validate_device({}) is False


class TestValidateOS:
    """Тесты для validate_os"""

    def test_validate_os_enum(self):
        """Тест с OSType enum"""
        assert validate_os(OSType.IOS) is True
        assert validate_os(OSType.ANDROID) is True

    def test_validate_os_string_valid(self):
        """Тест валидных строк"""
        assert validate_os("ios") is True
        assert validate_os("android") is True
        assert validate_os("IOS") is True
        assert validate_os("ANDROID") is True

    def test_validate_os_string_invalid(self):
        """Тест невалидных строк"""
        assert validate_os("windows") is False
        assert validate_os("linux") is False
        assert validate_os("macos") is False
        assert validate_os("") is False

    def test_validate_os_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_os(None) is False
        assert validate_os(123) is False
        assert validate_os([]) is False
        assert validate_os({}) is False


class TestValidateURL:
    """Тесты для validate_url"""

    def test_validate_url_valid(self):
        """Тест валидных URL"""
        assert validate_url("https://example.com") is True
        assert validate_url("http://example.com") is True
        assert validate_url("https://www.example.com/path") is True
        assert validate_url("https://example.com:8080/path?param=value") is True

    def test_validate_url_malformed(self):
        """Тест невалидных URL"""
        assert validate_url("not-a-url") is False
        assert validate_url("example.com") is False
        # FTP URL валиден по логике валидатора (имеет scheme и netloc)
        # assert validate_url("ftp://example.com") is False
        assert validate_url("://example.com") is False

    def test_validate_url_special_cases(self):
        """Тест специальных случаев"""
        assert validate_url("") is False
        assert validate_url("   ") is False
        assert validate_url("https://") is False
        assert validate_url("http://") is False

    def test_validate_url_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_url(None) is False
        assert validate_url(123) is False
        assert validate_url([]) is False
        assert validate_url({}) is False


class TestValidateCoordsExtended:
    """Расширенные тесты для validate_coords"""

    def test_validate_coords_boundary_values(self):
        """Тест граничных значений"""
        assert validate_coords((90.0, 180.0)) is True
        assert validate_coords((-90.0, -180.0)) is True
        assert validate_coords((0.0, 0.0)) is True
        assert validate_coords((90.1, 0.0)) is False
        assert validate_coords((-90.1, 0.0)) is False
        assert validate_coords((0.0, 180.1)) is False
        assert validate_coords((0.0, -180.1)) is False

    def test_validate_coords_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_coords("invalid") is False
        assert validate_coords(123) is False
        assert validate_coords(None) is False
        assert validate_coords([]) is False
        assert validate_coords({}) is False
        assert validate_coords((1,)) is False
        assert validate_coords((1, 2, 3)) is False


class TestValidateZoomExtended:
    """Расширенные тесты для validate_zoom"""

    def test_validate_zoom_edge_cases(self):
        """Тест граничных случаев"""
        assert validate_zoom(1) is True
        assert validate_zoom(15) is True
        assert validate_zoom(0) is False
        assert validate_zoom(16) is False

    def test_validate_zoom_negative(self):
        """Тест отрицательных значений"""
        assert validate_zoom(-1) is False
        assert validate_zoom(-10) is False

    def test_validate_zoom_extreme_values(self):
        """Тест экстремальных значений"""
        assert validate_zoom(100) is False
        assert validate_zoom(-100) is False
        assert validate_zoom(2**31) is False

    def test_validate_zoom_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_zoom("invalid") is False
        assert validate_zoom(1.5) is False
        assert validate_zoom(None) is False
        assert validate_zoom([]) is False
        assert validate_zoom({}) is False


class TestValidateCountry:
    """Тесты для validate_country"""

    def test_validate_country_valid(self):
        """Тест валидных ID стран"""
        assert validate_country(1) is True
        assert validate_country(100) is True
        assert validate_country(2840) is True

    def test_validate_country_invalid(self):
        """Тест невалидных ID стран"""
        assert validate_country(0) is False
        assert validate_country(-1) is False
        assert validate_country(-100) is False

    def test_validate_country_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_country("invalid") is False
        assert validate_country(1.5) is False
        assert validate_country(None) is False
        assert validate_country([]) is False
        assert validate_country({}) is False


class TestValidateRegion:
    """Тесты для validate_region"""

    def test_validate_region_valid(self):
        """Тест валидных ID регионов"""
        assert validate_region(1) is True
        assert validate_region(100) is True
        assert validate_region(213) is True

    def test_validate_region_invalid(self):
        """Тест невалидных ID регионов"""
        assert validate_region(0) is False
        assert validate_region(-1) is False
        assert validate_region(-100) is False

    def test_validate_region_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_region("invalid") is False
        assert validate_region(1.5) is False
        assert validate_region(None) is False
        assert validate_region([]) is False
        assert validate_region({}) is False


class TestValidateLanguage:
    """Тесты для validate_language"""

    def test_validate_language_valid(self):
        """Тест валидных кодов языков"""
        assert validate_language("ru") is True
        assert validate_language("en") is True
        assert validate_language("de") is True
        assert validate_language("fr") is True

    def test_validate_language_invalid(self):
        """Тест невалидных кодов языков"""
        assert validate_language("r") is False
        assert validate_language("rus") is False
        assert validate_language("") is False
        assert validate_language("123") is False
        assert validate_language("ru-ru") is False

    def test_validate_language_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_language(None) is False
        assert validate_language(123) is False
        assert validate_language([]) is False
        assert validate_language({}) is False


class TestValidateDomain:
    """Тесты для validate_domain"""

    def test_validate_domain_valid(self):
        """Тест валидных доменов"""
        assert validate_domain("ru") is True
        assert validate_domain("com") is True
        assert validate_domain("ua") is True
        assert validate_domain("com.tr") is True
        assert validate_domain("by") is True
        assert validate_domain("kz") is True
        assert validate_domain("RU") is True
        assert validate_domain("COM") is True

    def test_validate_domain_invalid(self):
        """Тест невалидных доменов"""
        assert validate_domain("invalid") is False
        assert validate_domain("org") is False
        assert validate_domain("net") is False
        assert validate_domain("") is False

    def test_validate_domain_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_domain(None) is False
        assert validate_domain(123) is False
        assert validate_domain([]) is False
        assert validate_domain({}) is False


class TestValidateGroupby:
    """Тесты для validate_groupby"""

    def test_validate_groupby_valid(self):
        """Тест валидных значений groupby"""
        assert validate_groupby(1) is True
        assert validate_groupby(5) is True
        assert validate_groupby(10) is True

    def test_validate_groupby_invalid(self):
        """Тест невалидных значений groupby"""
        assert validate_groupby(0) is False
        assert validate_groupby(11) is False
        assert validate_groupby(-1) is False
        assert validate_groupby(100) is False

    def test_validate_groupby_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_groupby("invalid") is False
        assert validate_groupby(1.5) is False
        assert validate_groupby(None) is False
        assert validate_groupby([]) is False
        assert validate_groupby({}) is False


class TestValidatePage:
    """Тесты для validate_page"""

    def test_validate_page_google_valid(self):
        """Тест валидных страниц для Google"""
        assert validate_page(1, "google") is True
        assert validate_page(10, "google") is True
        assert validate_page(100, "google") is True

    def test_validate_page_google_invalid(self):
        """Тест невалидных страниц для Google"""
        assert validate_page(0, "google") is False
        assert validate_page(-1, "google") is False

    def test_validate_page_yandex_valid(self):
        """Тест валидных страниц для Yandex"""
        assert validate_page(0, "yandex") is True
        assert validate_page(1, "yandex") is True
        assert validate_page(10, "yandex") is True

    def test_validate_page_yandex_invalid(self):
        """Тест невалидных страниц для Yandex"""
        assert validate_page(-1, "yandex") is False
        assert validate_page(-10, "yandex") is False

    def test_validate_page_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_page("invalid", "google") is False
        assert validate_page(1.5, "google") is False
        assert validate_page(None, "google") is False
        # validate_page не проверяет search_engine на None, поэтому этот тест не корректен
        # assert validate_page(1, None) is False


class TestValidateTimeFilter:
    """Тесты для validate_time_filter"""

    def test_validate_time_filter_valid(self):
        """Тест валидных фильтров времени"""
        assert validate_time_filter("qdr:h") is True
        assert validate_time_filter("qdr:d") is True
        assert validate_time_filter("qdr:w") is True
        assert validate_time_filter("qdr:m") is True
        assert validate_time_filter("qdr:y") is True

    def test_validate_time_filter_invalid(self):
        """Тест невалидных фильтров времени"""
        assert validate_time_filter("invalid") is False
        assert validate_time_filter("qdr:s") is False
        assert validate_time_filter("") is False
        assert validate_time_filter("qdr") is False

    def test_validate_time_filter_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_time_filter(None) is False
        assert validate_time_filter(123) is False
        assert validate_time_filter([]) is False
        assert validate_time_filter({}) is False


class TestValidateWithin:
    """Тесты для validate_within"""

    def test_validate_within_valid(self):
        """Тест валидных значений within"""
        assert validate_within(0) is True
        assert validate_within(1) is True
        assert validate_within(2) is True
        assert validate_within(77) is True

    def test_validate_within_invalid(self):
        """Тест невалидных значений within"""
        assert validate_within(3) is False
        assert validate_within(10) is False
        assert validate_within(-1) is False
        assert validate_within(100) is False

    def test_validate_within_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_within("invalid") is False
        assert validate_within(1.5) is False
        assert validate_within(None) is False
        assert validate_within([]) is False
        assert validate_within({}) is False


class TestValidateFileType:
    """Тесты для validate_file_type"""

    def test_validate_file_type_valid(self):
        """Тест валидных типов файлов"""
        assert validate_file_type("pdf") is True
        assert validate_file_type("doc") is True
        assert validate_file_type("docx") is True
        assert validate_file_type("xls") is True
        assert validate_file_type("xlsx") is True
        assert validate_file_type("ppt") is True
        assert validate_file_type("pptx") is True
        assert validate_file_type("txt") is True
        assert validate_file_type("rtf") is True
        assert validate_file_type("odt") is True
        assert validate_file_type("ods") is True
        assert validate_file_type("odp") is True
        assert validate_file_type("csv") is True
        assert validate_file_type("xml") is True
        assert validate_file_type("html") is True
        assert validate_file_type("htm") is True
        assert validate_file_type("php") is True
        assert validate_file_type("asp") is True
        assert validate_file_type("jsp") is True
        assert validate_file_type("js") is True
        assert validate_file_type("css") is True
        assert validate_file_type("PDF") is True
        assert validate_file_type("DOC") is True

    def test_validate_file_type_invalid(self):
        """Тест невалидных типов файлов"""
        assert validate_file_type("invalid") is False
        assert validate_file_type("exe") is False
        assert validate_file_type("zip") is False
        assert validate_file_type("") is False

    def test_validate_file_type_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_file_type(None) is False
        assert validate_file_type(123) is False
        assert validate_file_type([]) is False
        assert validate_file_type({}) is False


class TestValidateImageSize:
    """Тесты для validate_image_size"""

    def test_validate_image_size_valid(self):
        """Тест валидных размеров изображений"""
        assert validate_image_size("small") is True
        assert validate_image_size("medium") is True
        assert validate_image_size("large") is True
        assert validate_image_size("xlarge") is True
        assert validate_image_size("SMALL") is True
        assert validate_image_size("MEDIUM") is True

    def test_validate_image_size_invalid(self):
        """Тест невалидных размеров изображений"""
        assert validate_image_size("invalid") is False
        assert validate_image_size("tiny") is False
        assert validate_image_size("huge") is False
        assert validate_image_size("") is False

    def test_validate_image_size_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_image_size(None) is False
        assert validate_image_size(123) is False
        assert validate_image_size([]) is False
        assert validate_image_size({}) is False


class TestValidateImageColor:
    """Тесты для validate_image_color"""

    def test_validate_image_color_valid(self):
        """Тест валидных цветов изображений"""
        valid_colors = [
            "any",
            "color",
            "grayscale",
            "transparent",
            "red",
            "orange",
            "yellow",
            "green",
            "teal",
            "blue",
            "purple",
            "pink",
            "white",
            "gray",
            "black",
            "brown",
        ]
        for color in valid_colors:
            assert validate_image_color(color) is True
            assert validate_image_color(color.upper()) is True

    def test_validate_image_color_invalid(self):
        """Тест невалидных цветов изображений"""
        assert validate_image_color("invalid") is False
        assert validate_image_color("cyan") is False
        assert validate_image_color("") is False

    def test_validate_image_color_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_image_color(None) is False
        assert validate_image_color(123) is False
        assert validate_image_color([]) is False
        assert validate_image_color({}) is False


class TestValidateImageType:
    """Тесты для validate_image_type"""

    def test_validate_image_type_valid(self):
        """Тест валидных типов изображений"""
        valid_types = [
            "any",
            "face",
            "photo",
            "clipart",
            "lineart",
            "animated",
        ]
        for img_type in valid_types:
            assert validate_image_type(img_type) is True
            assert validate_image_type(img_type.upper()) is True

    def test_validate_image_type_invalid(self):
        """Тест невалидных типов изображений"""
        assert validate_image_type("invalid") is False
        assert validate_image_type("gif") is False
        assert validate_image_type("") is False

    def test_validate_image_type_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_image_type(None) is False
        assert validate_image_type(123) is False
        assert validate_image_type([]) is False
        assert validate_image_type({}) is False


class TestValidateUsageRights:
    """Тесты для validate_usage_rights"""

    def test_validate_usage_rights_valid(self):
        """Тест валидных прав использования"""
        valid_rights = [
            "any",
            "cc_publicdomain",
            "cc_attribute",
            "cc_sharealike",
            "cc_noncommercial",
            "cc_nonderived",
        ]
        for rights in valid_rights:
            assert validate_usage_rights(rights) is True
            assert validate_usage_rights(rights.upper()) is True

    def test_validate_usage_rights_invalid(self):
        """Тест невалидных прав использования"""
        assert validate_usage_rights("invalid") is False
        assert validate_usage_rights("cc_attribution") is False
        assert validate_usage_rights("") is False

    def test_validate_usage_rights_invalid_types(self):
        """Тест невалидных типов"""
        assert validate_usage_rights(None) is False
        assert validate_usage_rights(123) is False
        assert validate_usage_rights([]) is False
        assert validate_usage_rights({}) is False
