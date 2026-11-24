import streamlit as st
import pandas as pd
import db

db.init_db()

st.sidebar.title("Dev Tools")
page = st.sidebar.radio("Навігація:", ["Головна (Каталог)", "Додати бібліотеку", "Про автора"])

if page == "Головна (Каталог)":
    st.title("Каталог бібліотек та фреймворків Python")
    st.write("Переглядайте, шукайте та фільтруйте корисні інструменти для розробки.")

    categories = db.get_categories()
    cat_names = ["Усі"] + [cat[1] for cat in categories]
    
    col1, col2 = st.columns(2)
    with col1:
        search_query = st.text_input("Пошук за назвою або описом")
    with col2:
        selected_category = st.selectbox("Фільтр за категорією", cat_names)
        
    libraries = db.get_libraries(search_query, selected_category)
    
    if libraries:
        df = pd.DataFrame(libraries, columns=["ID", "Назва", "Сайт / Документація", "Опис", "Корисність (1-5)", "Категорія"])
        st.dataframe(df, use_container_width=True)
        st.caption(f"Знайдено записів: {len(df)}")
    else:
        st.warning("Нічого не знайдено за вашим запитом.")

elif page == "Додати бібліотеку":
    st.title("Додати новий інструмент")
    
    categories = db.get_categories()
    cat_dict = {name: cat_id for cat_id, name in categories}
    
    with st.form("add_library_form"):
        name = st.text_input("Назва бібліотеки / фреймворку")
        url = st.text_input("Посилання на офіційний сайт або документацію")
        description = st.text_area("Короткий опис призначення")
        rating = st.slider("Оцінка корисності (від 1 до 5)", 1, 5, 5)
        category_name = st.selectbox("Категорія", list(cat_dict.keys()))
        
        submitted = st.form_submit_button("Зберегти у базу даних")
        
        if submitted:
            if name and url and description:
                db.add_library(name, url, description, rating, cat_dict[category_name])
                st.success(f"Бібліотеку «{name}» успішно додано до каталогу!")
            else:
                st.error("Будь ласка, заповніть усі обов'язкові поля.")

elif page == "Про автора":
    st.title("Про автора")
    st.write("**Виконала:** Студентка групи П-31 Смотрицька Анастасія")
    st.write("**Тема:** Каталог бібліотек Python / Фреймворків (Dev Tools)")
    st.markdown("---")