"""Halaman riwayat hasil screener dari folder data/results/."""

from datetime import datetime
from pathlib import Path
import re

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

RESULTS_DIR = Path(__file__).parent.parent.parent / "data" / "results"


def _list_result_files() -> list:
    """Scan data/results/ for CSV files and return sorted list of paths."""
    if not RESULTS_DIR.exists():
        return []
    files = sorted(RESULTS_DIR.glob("*.csv"), reverse=True)
    return list(files)


def _extract_result_metadata(filepath: Path) -> dict:
    """Extract source, timestamp, and display label from result filename."""
    stem = filepath.stem
    stem_lower = stem.lower()

    source = "Unknown"
    if "_bei_" in stem_lower:
        source = "BEI"
    elif "_yahoo_" in stem_lower:
        source = "Yahoo"

    timestamp = None
    match_legacy = re.search(r"(\d{8})_(\d{6})$", stem)
    match_new = re.search(r"(\d{2}-\d{2}-\d{4})_(\d{6})$", stem)

    if match_legacy:
        try:
            timestamp = datetime.strptime(
                f"{match_legacy.group(1)}_{match_legacy.group(2)}",
                "%Y%m%d_%H%M%S",
            )
        except ValueError:
            timestamp = None
    elif match_new:
        try:
            timestamp = datetime.strptime(
                f"{match_new.group(1)}_{match_new.group(2)}",
                "%d-%m-%Y_%H%M%S",
            )
        except ValueError:
            timestamp = None

    if timestamp is not None:
        label = f"{timestamp.strftime('%d-%m-%Y %H:%M:%S')} ({source})"
    else:
        clean_stem = stem
        for prefix in ("results_", "screener_", "scan_"):
            clean_stem = clean_stem.replace(prefix, "")
        label = clean_stem

    return {
        "source": source,
        "timestamp": timestamp,
        "label": label,
    }


@st.cache_data(ttl=120)
def _read_result_csv(filepath: str) -> pd.DataFrame:
    """Read one historical result file with short-lived cache."""
    return pd.read_csv(filepath)


def render_history() -> None:
    """Render the historical results page."""
    st.title("📅 Riwayat Hasil Screener")
    st.markdown(
        f"Tampilkan hasil scan historis dari folder `data/results/`. "
        "File disimpan otomatis oleh GitHub Actions setiap hari."
    )
    st.divider()

    result_files = _list_result_files()

    if not result_files:
        st.info(
            "Belum ada file hasil historis. "
            "File akan tersedia setelah GitHub Actions menjalankan scan harian. "
            f"\n\nDirektori yang dipindai: `{RESULTS_DIR}`"
        )
        return

    # Date selector
    file_labels = [_extract_result_metadata(f)["label"] for f in result_files]
    selected_label = st.selectbox(
        "Pilih Tanggal",
        options=file_labels,
        index=0,
        help="Pilih tanggal scan untuk ditampilkan",
    )

    selected_idx = file_labels.index(selected_label)
    selected_file = result_files[selected_idx]

    # Load selected file
    try:
        df = _read_result_csv(str(selected_file))
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        return

    # Summary for selected date
    total = len(df)
    ma_tight_count = int(df["MA_Tight"].sum()) if "MA_Tight" in df.columns else 0
    signal_count = int(df["Signal"].sum()) if "Signal" in df.columns else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Saham", total)
    col2.metric("MA Tight", ma_tight_count)
    col3.metric("Sinyal", signal_count)

    st.divider()

    # Filters for selected date result
    st.subheader("🔍 Filter Hasil")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_ma = st.multiselect(
            "Filter Status MA",
            options=["MA Tight", "Tidak MA Tight"],
            default=["MA Tight", "Tidak MA Tight"],
            help="Filter berdasarkan kondisi MA Kuncup/MA Ketat",
        )
    with col_f2:
        filter_signal = st.multiselect(
            "Filter Status Sinyal",
            options=["Sinyal Aktif", "Belum Sinyal"],
            default=["Sinyal Aktif", "Belum Sinyal"],
            help="Filter berdasarkan status sinyal entry",
        )

    filtered_df = df.copy()

    if "MA_Tight" in filtered_df.columns and filter_ma:
        if "MA Tight" in filter_ma and "Tidak MA Tight" not in filter_ma:
            filtered_df = filtered_df[filtered_df["MA_Tight"].eq(True)]
        elif "Tidak MA Tight" in filter_ma and "MA Tight" not in filter_ma:
            filtered_df = filtered_df[filtered_df["MA_Tight"].eq(False)]

    if "Signal" in filtered_df.columns and filter_signal:
        if "Sinyal Aktif" in filter_signal and "Belum Sinyal" not in filter_signal:
            filtered_df = filtered_df[filtered_df["Signal"].eq(True)]
        elif "Belum Sinyal" in filter_signal and "Sinyal Aktif" not in filter_signal:
            filtered_df = filtered_df[filtered_df["Signal"].eq(False)]

    st.caption(f"Menampilkan {len(filtered_df)} dari {len(df)} saham pada file terpilih.")

    st.divider()

    # Table for selected date
    st.subheader(f"📋 Hasil Scan: {selected_label}")
    if not filtered_df.empty:
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name=selected_file.name,
            mime="text/csv",
        )
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada data yang sesuai dengan filter.")

    st.divider()

    # Signal trend chart across all dates
    st.subheader("📈 Tren Jumlah Sinyal per Scan")

    trend_data = []
    for filepath in result_files:
        try:
            temp_df = _read_result_csv(str(filepath))
            signals = int(temp_df["Signal"].sum()) if "Signal" in temp_df.columns else 0
            metadata = _extract_result_metadata(filepath)
            trend_data.append({
                "Label": metadata["label"],
                "Waktu": metadata["timestamp"],
                "Sumber": metadata["source"],
                "Sinyal": signals,
            })
        except Exception:
            continue

    if trend_data:
        trend_df = pd.DataFrame(trend_data)
        trend_df["Waktu"] = pd.to_datetime(trend_df["Waktu"], errors="coerce")

        if trend_df["Waktu"].notna().any():
            trend_df["Tanggal"] = trend_df["Waktu"].dt.strftime("%d-%m-%Y")
            trend_df["Tanggal_Sort"] = trend_df["Waktu"].dt.strftime("%Y-%m-%d")
            trend_df = trend_df.sort_values(["Waktu", "Label"])
        else:
            trend_df = trend_df.sort_values("Label")
            trend_df["Tanggal"] = trend_df["Label"].astype(str).str[:10]
            trend_df["Tanggal_Sort"] = trend_df["Tanggal"]

        pivot_df = (
            trend_df.pivot_table(
                index=["Tanggal_Sort", "Tanggal"],
                columns="Sumber",
                values="Sinyal",
                aggfunc="sum",
                fill_value=0,
            )
            .sort_index(level=0)
            .reset_index()
        )

        source_colors = {
            "BEI": "#00bfff",
            "Yahoo": "#00c864",
            "Unknown": "#a0a0a0",
        }

        fig = go.Figure()
        for source in ["BEI", "Yahoo", "Unknown"]:
            if source in pivot_df.columns:
                y_values = pivot_df[source]
                fig.add_trace(
                    go.Bar(
                        x=pivot_df["Tanggal"],
                        y=y_values,
                        name=source,
                        marker_color=source_colors.get(source, "#00bfff"),
                        text=[str(int(v)) if float(v) > 0 else "" for v in y_values],
                        textposition="outside",
                        cliponaxis=False,
                    )
                )

        fig.update_layout(
            template="plotly_dark",
            height=300,
            xaxis_title="Tanggal",
            yaxis_title="Jumlah Sinyal",
            margin=dict(l=0, r=0, t=10, b=0),
            barmode="group",
            showlegend=True,
            legend_title_text="Sumber",
        )
        fig.update_xaxes(type="category", tickangle=0)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak cukup data untuk menampilkan tren.")

    # Footer
    st.divider()
    st.caption(
        "⚠️ **Disclaimer**: Data historis ini hanya untuk tujuan edukasi. "
        "Bukan merupakan rekomendasi investasi."
    )
