from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mdm_file = request.files["mdm"]
        scm1_file = request.files["scm1"]
        scm2_file = request.files["scm2"]

        mdm_path = os.path.join(UPLOAD_FOLDER, mdm_file.filename)
        scm1_path = os.path.join(UPLOAD_FOLDER, scm1_file.filename)
        scm2_path = os.path.join(UPLOAD_FOLDER, scm2_file.filename)

        mdm_file.save(mdm_path)
        scm1_file.save(scm1_path)
        scm2_file.save(scm2_path)

        # ===============================
        # YOUR LOGIC STARTS (UNCHANGED)
        # ===============================

        df1 = pd.read_csv(mdm_path)
        df1_filtered = df1[df1["NOTIFICATION"] != "Reconnection"]

        df1_unique = df1_filtered.sort_values(["NOTIFICATION"]).drop_duplicates(
            subset=["NOTIFICATION", "CONSUMER_UDC_ID"],
            keep="first"
        )

        def process_scm(file_path):
            df = pd.read_csv(file_path)
            group_col = df.columns[13]

            allowed = [
                "AFTER_METER_COMMISSIONING",
                "AFTER_DISCONNECTION",
                "DAILY_BALANCE",
                "DISCONNECTION_NOTICE",
                "DISCONNECTION_NOTICE_LAST"
            ]

            df = df[df[group_col].isin(allowed)]
            df = df.iloc[:, [df.columns.get_loc("Consumer Number"), 13]]
            df.columns = ["Consumer Number", "SCM_Status"]
            return df

        scm1 = process_scm(scm1_path)
        scm2 = process_scm(scm2_path)

        def merge_logic(base, scm):
            g1 = {
                "Credit Low": "DAILY_BALANCE",
                "Welcome": "AFTER_METER_COMMISSIONING",
                "Disconnection": "AFTER_DISCONNECTION",
                "Future Disconnection": "DISCONNECTION_NOTICE",
                "Imminent Disconnection": "DISCONNECTION_NOTICE_LAST"
            }

            result = []

            for k, v in g1.items():
                m = base[base["NOTIFICATION"] == k].merge(
                    scm[scm["SCM_Status"] == v],
                    how="left",
                    left_on="CONSUMER_UDC_ID",
                    right_on="Consumer Number"
                )
                result.append(m)

            final = pd.concat(result, ignore_index=True)
            return final.drop(columns=["Consumer Number"], errors="ignore")

        final1 = merge_logic(df1_unique, scm1)
        final2 = merge_logic(final1, scm2)

        output_path = os.path.join(OUTPUT_FOLDER, "Final_Report.xlsx")
        final2.to_excel(output_path, index=False)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
