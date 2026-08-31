import html
import json
from datetime import datetime


class ReportHelper:

    # ======================================================
    # BUILD HTML
    # ======================================================

    @classmethod
    def build_html(
        cls,
        suite_name,
        results,
        total,
        passed,
        failed,
        duration
    ):

        rows = ""

        # ==================================================
        # RESULT ROWS
        # ==================================================

        for index, result in enumerate(
            results,
            start=1
        ):

            # ==============================================
            # BASIC INFORMATION
            # ==============================================

            status = result.get(
                "status",
                "UNKNOWN"
            )

            status_class = str(
                status
            ).lower()

            test_case = cls._escape(
                result.get(
                    "test_case",
                    ""
                )
            )

            scenario = cls._escape(
                result.get(
                    "scenario",
                    ""
                )
            )

            description = cls._escape(
                result.get(
                    "description",
                    ""
                )
            )

            method = cls._escape(
                result.get(
                    "method",
                    ""
                )
            )

            url = cls._escape(
                result.get(
                    "url",
                    ""
                )
            )

            duration_ms = result.get(
                "duration_ms",
                result.get(
                    "duration",
                    0
                )
            )

            # ==============================================
            # REQUEST
            # ==============================================

            request_headers = cls._format_data(
                result.get(
                    "request_headers",
                    {}
                )
            )

            request_body = cls._format_data(
                result.get(
                    "request_body"
                )
            )

            # ==============================================
            # RESPONSE
            # ==============================================

            response_status = cls._escape(
                result.get(
                    "response_status",
                    ""
                )
            )

            response_headers = cls._format_data(
                result.get(
                    "response_headers",
                    {}
                )
            )

            response_body = cls._format_data(
                result.get(
                    "response_body"
                )
            )

            # ==============================================
            # ERROR
            # ==============================================

            error_section = cls._build_error(
                result.get(
                    "error"
                )
            )

            # ==============================================
            # FAILED ASSERTIONS ONLY
            # ==============================================

            assertion_section = cls._build_assertions(
                result.get(
                    "assertions",
                    []
                )
            )

            # ==============================================
            # MAIN ROW
            # ==============================================

            rows += f"""
            <tr
                class="scenario-row"
                onclick="toggleDetail('detail-{index}')"
            >

                <td>
                    {index}
                </td>

                <td>
                    <strong>
                        {test_case}
                    </strong>
                </td>

                <td>
                    <span class="scenario-link">
                        {scenario}
                    </span>
                </td>

                <td>
                    {description}
                </td>

                <td>
                    {duration_ms} ms
                </td>

                <td>
                    <span
                        class="status {status_class}"
                    >
                        {status}
                    </span>
                </td>

            </tr>

            <tr
                id="detail-{index}"
                class="detail-row"
            >

                <td colspan="6">

                    <div class="detail-container">

                        <!-- BASIC INFO -->

                        <div class="request-info">

                            <div class="info-item">

                                <span>
                                    Method
                                </span>

                                <strong>
                                    {method}
                                </strong>

                            </div>

                            <div
                                class="info-item url-item"
                            >

                                <span>
                                    URL
                                </span>

                                <strong>
                                    {url}
                                </strong>

                            </div>

                            <div class="info-item">

                                <span>
                                    Response Time
                                </span>

                                <strong>
                                    {duration_ms} ms
                                </strong>

                            </div>

                            <div class="info-item">

                                <span>
                                    Response Status
                                </span>

                                <strong>
                                    {response_status}
                                </strong>

                            </div>

                        </div>

                        <!-- ERROR -->

                        {error_section}

                        <!-- FAILED ASSERTIONS -->

                        {assertion_section}

                        <!-- REQUEST HEADERS -->

                        <div class="detail-section">

                            <h3>
                                Request Headers
                            </h3>

                            <pre>{request_headers}</pre>

                        </div>

                        <!-- REQUEST BODY -->

                        <div class="detail-section">

                            <h3>
                                Request Body
                            </h3>

                            <pre>{request_body}</pre>

                        </div>

                        <!-- RESPONSE HEADERS -->

                        <div class="detail-section">

                            <h3>
                                Response Headers
                            </h3>

                            <pre>{response_headers}</pre>

                        </div>

                        <!-- RESPONSE BODY -->

                        <div class="detail-section">

                            <h3>
                                Response Body
                            </h3>

                            <pre>{response_body}</pre>

                        </div>

                    </div>

                </td>

            </tr>
            """

        suite_name = cls._escape(
            suite_name
        )

        generated_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # ==================================================
        # HTML
        # ==================================================

        return f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>
    {suite_name} Report
</title>

<style>

/* ======================================================
   BODY
   ====================================================== */

body {{

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    margin:
        0;

    padding:
        30px;

    background:
        #f5f6f8;
}}


/* ======================================================
   CONTAINER
   ====================================================== */

.container {{

    max-width:
        1400px;

    margin:
        auto;
}}


/* ======================================================
   HEADER
   ====================================================== */

.header {{

    background:
        white;

    padding:
        25px;

    border-radius:
        8px;

    margin-bottom:
        20px;
}}

.header h1 {{

    margin:
        0 0 10px 0;
}}


/* ======================================================
   SUMMARY
   ====================================================== */

.summary {{

    display:
        flex;

    gap:
        15px;

    margin-bottom:
        20px;
}}

.card {{

    background:
        white;

    padding:
        20px;

    border-radius:
        8px;

    min-width:
        130px;
}}

.card .number {{

    font-size:
        28px;

    font-weight:
        bold;
}}


/* ======================================================
   TABLE
   ====================================================== */

.table-container {{

    background:
        white;

    border-radius:
        8px;

    padding:
        20px;

    overflow-x:
        auto;
}}

table {{

    width:
        100%;

    border-collapse:
        collapse;
}}

th {{

    text-align:
        left;

    background:
        #f0f1f3;

    padding:
        12px;
}}

td {{

    padding:
        12px;

    border-bottom:
        1px solid #eee;
}}


/* ======================================================
   SCENARIO
   ====================================================== */

.scenario-row {{

    cursor:
        pointer;

    transition:
        background 0.15s ease;
}}

.scenario-row:hover {{

    background:
        #f5f7fa;
}}

.scenario-link {{

    font-weight:
        600;
}}


/* ======================================================
   STATUS
   ====================================================== */

.status {{

    padding:
        5px 10px;

    border-radius:
        5px;

    font-weight:
        bold;

    display:
        inline-block;
}}

.passed {{

    background:
        #d4edda;

    color:
        #155724;
}}

.failed {{

    background:
        #f8d7da;

    color:
        #721c24;
}}

.unknown {{

    background:
        #e2e3e5;

    color:
        #383d41;
}}


/* ======================================================
   DETAIL
   ====================================================== */

.detail-row {{

    display:
        none;
}}

.detail-row.open {{

    display:
        table-row;
}}

.detail-container {{

    padding:
        20px;

    background:
        #fafafa;
}}


/* ======================================================
   REQUEST INFO
   ====================================================== */

.request-info {{

    display:
        flex;

    gap:
        30px;

    margin-bottom:
        20px;

    padding:
        15px;

    background:
        white;

    border-radius:
        6px;

    border:
        1px solid #eee;
}}

.info-item {{

    display:
        flex;

    flex-direction:
        column;

    gap:
        5px;

    min-width:
        120px;
}}

.info-item span {{

    font-size:
        12px;

    color:
        #777;

    text-transform:
        uppercase;
}}

.info-item strong {{

    word-break:
        break-all;
}}

.url-item {{

    flex:
        1;
}}


/* ======================================================
   ERROR
   ====================================================== */

.error-section {{

    margin-top:
        20px;

    padding:
        15px;

    background:
        #fff5f5;

    border:
        1px solid #f5c2c7;

    border-radius:
        6px;
}}

.error-title {{

    color:
        #842029;

    font-weight:
        bold;

    font-size:
        15px;

    margin-bottom:
        10px;
}}

.error-section pre {{

    background:
        #2b1e1e;

    color:
        #ffb3b3;

    margin:
        0;

    padding:
        15px;

    border-radius:
        5px;

    white-space:
        pre-wrap;

    word-break:
        break-word;

    font-family:
        Consolas,
        "Courier New",
        monospace;

    font-size:
        13px;

    line-height:
        1.5;
}}


/* ======================================================
   ASSERTIONS
   ====================================================== */

.assertion-section {{

    margin-top:
        20px;

    padding:
        15px;

    background:
        #fff5f5;

    border:
        1px solid #f5c2c7;

    border-radius:
        6px;
}}

.assertion-title {{

    color:
        #842029;

    font-weight:
        bold;

    font-size:
        15px;

    margin-bottom:
        12px;
}}

.assertion-count {{

    font-weight:
        normal;

    color:
        #dc3545;
}}

.assertion-item {{

    padding:
        12px;

    margin-bottom:
        8px;

    background:
        white;

    border-radius:
        5px;

    border-left:
        4px solid #dc3545;
}}

.assertion-item:last-child {{

    margin-bottom:
        0;
}}

.assertion-status {{

    color:
        #dc3545;

    font-weight:
        bold;

    margin-bottom:
        6px;
}}

.assertion-field {{

    font-weight:
        bold;

    margin-bottom:
        5px;
}}

.assertion-message {{

    margin-bottom:
        8px;

    color:
        #555;
}}

.assertion-value {{

    margin-top:
        5px;

    font-family:
        Consolas,
        "Courier New",
        monospace;

    font-size:
        13px;

    word-break:
        break-word;
}}

.expected-label {{

    color:
        #6c757d;

    font-weight:
        bold;
}}

.actual-label {{

    color:
        #dc3545;

    font-weight:
        bold;
}}


/* ======================================================
   DETAIL SECTION
   ====================================================== */

.detail-section {{

    margin-top:
        20px;
}}

.detail-section h3 {{

    margin:
        0 0 8px 0;

    font-size:
        15px;
}}


/* ======================================================
   CODE BLOCK
   ====================================================== */

.detail-section pre {{

    background:
        #1e1e1e;

    color:
        #f5f5f5;

    padding:
        15px;

    border-radius:
        6px;

    overflow-x:
        auto;

    white-space:
        pre-wrap;

    word-break:
        break-word;

    font-family:
        Consolas,
        "Courier New",
        monospace;

    font-size:
        13px;

    line-height:
        1.5;

    margin:
        0;
}}


/* ======================================================
   RESPONSIVE
   ====================================================== */

@media (max-width: 900px) {{

    .request-info {{

        flex-direction:
            column;

        gap:
            15px;
    }}

    .summary {{

        flex-wrap:
            wrap;
    }}

}}

</style>

</head>

<body>

<div class="container">

    <!-- HEADER -->

    <div class="header">

        <h1>
            {suite_name}
        </h1>

        <div>
            Generated:
            {generated_time}
        </div>

        <div>
            Duration:
            {duration:.2f} seconds
        </div>

    </div>


    <!-- SUMMARY -->

    <div class="summary">

        <div class="card">

            <div>
                Total
            </div>

            <div class="number">
                {total}
            </div>

        </div>

        <div class="card">

            <div>
                Passed
            </div>

            <div class="number">
                {passed}
            </div>

        </div>

        <div class="card">

            <div>
                Failed
            </div>

            <div class="number">
                {failed}
            </div>

        </div>

    </div>


    <!-- TABLE -->

    <div class="table-container">

        <table>

            <thead>

                <tr>

                    <th>
                        No
                    </th>

                    <th>
                        Test Case
                    </th>

                    <th>
                        Scenario
                    </th>

                    <th>
                        Description
                    </th>

                    <th>
                        Duration
                    </th>

                    <th>
                        Status
                    </th>

                </tr>

            </thead>

            <tbody>

                {rows}

            </tbody>

        </table>

    </div>

</div>


<script>

function toggleDetail(id) {{

    const element =
        document.getElementById(id);

    if (
        element.classList.contains("open")
    ) {{

        element.classList.remove("open");

    }} else {{

        element.classList.add("open");

    }}

}}

</script>

</body>

</html>
"""

    # ======================================================
    # BUILD ERROR
    # ======================================================

    @classmethod
    def _build_error(
        cls,
        error
    ):

        if not error:
            return ""

        error_message = cls._format_data(
            error
        )

        return f"""
        <div class="error-section">

            <div class="error-title">
                ❌ Error
            </div>

            <pre>{error_message}</pre>

        </div>
        """

    # ======================================================
    # BUILD FAILED ASSERTIONS
    # ======================================================

    @classmethod
    def _build_assertions(
        cls,
        assertions
    ):

        if not assertions:
            return ""

        failed_assertions = [

            assertion

            for assertion in assertions

            if not assertion.get(
                "passed",
                False
            )

        ]

        if not failed_assertions:
            return ""

        items = ""

        for assertion in failed_assertions:

            field = cls._escape(
                assertion.get(
                    "field",
                    ""
                )
            )

            message = cls._escape(
                assertion.get(
                    "message",
                    ""
                )
            )

            expected = cls._format_data(
                assertion.get(
                    "expected"
                )
            )

            actual = cls._format_data(
                assertion.get(
                    "actual"
                )
            )

            field_html = ""

            if field:

                field_html = f"""
                <div class="assertion-field">
                    {field}
                </div>
                """

            message_html = ""

            if message:

                message_html = f"""
                <div class="assertion-message">
                    {message}
                </div>
                """

            items += f"""
            <div class="assertion-item">

                <div class="assertion-status">
                    ✗ FAILED
                </div>

                {field_html}

                {message_html}

                <div class="assertion-value">

                    <span class="expected-label">
                        Expected:
                    </span>

                    {expected}

                </div>

                <div class="assertion-value">

                    <span class="actual-label">
                        Actual:
                    </span>

                    {actual}

                </div>

            </div>
            """

        return f"""
        <div class="assertion-section">

            <div class="assertion-title">

                ⚠ Assertions Failed

                <span class="assertion-count">
                    ({len(failed_assertions)})
                </span>

            </div>

            {items}

        </div>
        """

    # ======================================================
    # ESCAPE HTML
    # ======================================================

    @staticmethod
    def _escape(
        value
    ):

        if value is None:
            return ""

        return html.escape(
            str(value)
        )

    # ======================================================
    # FORMAT DATA
    # ======================================================

    @staticmethod
    def _format_data(
        value
    ):

        if value is None:
            return ""

        try:

            if isinstance(
                value,
                (dict, list)
            ):

                value = json.dumps(
                    value,
                    indent=4,
                    ensure_ascii=False
                )

            return html.escape(
                str(value)
            )

        except Exception:

            return html.escape(
                str(value)
            )
