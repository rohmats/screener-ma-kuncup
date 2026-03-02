"""Halaman riwayat hasil screener dari folder data/results/."""

import os
from pathlib import Path

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


def _extract_date_from_filename(filepath: Path) -> str:
    """Extract a human-readable date label from filename (e.g. results_2024-01-15.csv)."""
    stem = filepath.stem
    # Remove common prefixes
    for prefix in ("results_", "screener_", "scan_"):
        stem = stem.replace(prefix, "")
    return stem


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
    file_labels = [_extract_date_from_filename(f) for f in result_files]
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
        df = pd.read_csv(selected_file)
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

    # Table for selected date
    st.subheader(f"📋 Hasil Scan: {selected_label}")
    if not df.empty:
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name=selected_file.name,
            mime="text/csv",
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("File kosong.")

    st.divider()

    # Signal trend chart across all dates
    st.subheader("📈 Tren Jumlah Sinyal per Hari")

    trend_data = []
    for filepath in result_files:
        try:
            temp_df = pd.read_csv(filepath)
            signals = int(temp_df["Signal"].sum()) if "Signal" in temp_df.columns else 0
            trend_data.append({
                "Tanggal": _extract_date_from_filename(filepath),
                "Sinyal": signals,
            })
        except Exception:
            continue

    if trend_data:
        trend_df = pd.DataFrame(trend_data).sort_values("Tanggal")
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=trend_df["Tanggal"],
                y=trend_df["Sinyal"],
                mode="lines+markers",
                name="Jumlah Sinyal",
                line=dict(color="#00bfff", width=2),
                marker=dict(size=6),
            )
        )
        fig.update_layout(
            template="plotly_dark",
            height=300,
            xaxis_title="Tanggal",
            yaxis_title="Jumlah Sinyal",
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak cukup data untuk menampilkan tren.")

    # Footer
    st.divider()
    st.caption(
        "⚠️ **Disclaimer**: Data historis ini hanya untuk tujuan edukasi. "
        "Bukan merupakan rekomendasi investasi."
    )
