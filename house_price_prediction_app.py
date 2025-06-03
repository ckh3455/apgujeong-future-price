import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 📥 데이터 로드
file_path = '단지 연도별 최대값.xlsx'df = pd.read_excel(file_path)
df.columns = df.columns.astype(str)

# 📌 앱 제목
st.title("🏠 단지별 목표 금액 도달 예상일 계산기")

# 📢 압구정 원 부동산중개
st.sidebar.header("압구정 원 부동산중개")
contact_number = st.sidebar.text_input("전화번호", "02-540-3334")
agent_name = st.sidebar.text_input("개발자", "최규호 이사")
st.sidebar.markdown(f"📱 {contact_number}\n👤 {agent_name}")

# 📅 입력 정보
st.sidebar.header("입력 정보")
단지목록 = df['단지명_평형'].unique()
selected_complex = st.sidebar.selectbox("🏢 단지 선택", 단지목록)
신고가_날짜 = st.sidebar.date_input("신고가 기록 날짜", datetime.today())
신고가_금액 = st.sidebar.text_input("신고가 금액 (억)", value="")
목표_금액 = st.sidebar.text_input("목표 금액 (억)", value="")

# 📘 사용법 안내
st.sidebar.markdown("📘 **사용법**\n\n"
                    "1️⃣ **단지 선택**: 화살표를 눌러 단지를 선택합니다.\n\n"
                    "2️⃣ **신고가 금액**: 새로운 신고가 금액을 기록한 날짜와 금액을 (억) 단위로 입력합니다.\n"
                    "   예) 85\n\n"
                    "3️⃣ **목표 금액**: 원하는 목표 금액을 (억) 단위로 입력합니다.\n"
                    "   예) 100")

# 연도 리스트 (2015~2024)
연도_리스트 = [str(y) for y in range(2015, 2025)]

# 선택 단지 데이터 추출
selected_data = df[df['단지명_평형'] == selected_complex]
if selected_data.empty:
    st.warning("선택한 단지의 데이터가 없습니다.")
else:
    상승률_리스트 = []
    for i in range(len(연도_리스트) - 1):
        이전 = 연도_리스트[i]
        다음 = 연도_리스트[i+1]
        try:
            이전값 = selected_data.iloc[0][이전]
            다음값 = selected_data.iloc[0][다음]
            if pd.notnull(이전값) and pd.notnull(다음값) and 이전값 > 0:
                상승률 = (다음값 - 이전값) / 이전값
                상승률_리스트.append(상승률)
        except:
            continue
    
    if 상승률_리스트:
        연평균_상승률 = sum(상승률_리스트) / len(상승률_리스트)
        st.write(f"📈 선택한 단지: {selected_complex}")
        st.write(f"📈 최근 연평균 상승률: {연평균_상승률 * 100:.2f}%")
        
        if 신고가_금액.strip() != "" and 목표_금액.strip() != "":
            try:
                신고가_금액 = float(신고가_금액)
                목표_금액 = float(목표_금액)
                
                if 신고가_금액 > 0 and 목표_금액 > 신고가_금액 and 연평균_상승률 > 0:
                    신고가_만원 = 신고가_금액 * 10000
                    목표_만원 = 목표_금액 * 10000

                    년수_예상 = 0
                    현재_금액 = 신고가_만원
                    while 현재_금액 < 목표_만원:
                        현재_금액 *= (1 + 연평균_상승률)
                        년수_예상 += 1
                    예상_도달일 = 신고가_날짜 + timedelta(days=년수_예상 * 365)

                    def format_money(amount):
                        return f"{amount:.1f}" if amount % 1 != 0 else f"{int(amount)}"

                    st.success(f"🎯 선택한 단지: {selected_complex}\n"
                               f"신고가 금액: {format_money(신고가_금액)}억\n"
                               f"목표 금액: {format_money(목표_금액)}억\n"
                               f"평균 연간 상승률: {연평균_상승률 * 100:.2f}%\n"
                               f"예상 도달일: {예상_도달일.year}년 {예상_도달일.month}월 {예상_도달일.day}일")
                else:
                    st.warning("🚨 목표 금액은 신고가 금액보다 높아야 하고, 상승률이 0보다 커야 합니다.")
            except ValueError:
                st.warning("🚨 금액 입력란에는 숫자만 입력하세요.")
        else:
            st.info("💬 신고가 금액과 목표 금액을 입력하면 결과가 표시됩니다.")
    else:
        st.warning("📉 선택한 단지의 연도별 상승률 데이터가 부족합니다.")
