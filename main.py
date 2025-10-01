from domain.category import Category 

print("--- TESTE 1: Serialização (to_dict / from_dict) ---")

cat_original = Category(name="Música", description="Álbuns e Instrumentos", is_active=True)
cat_original.clear_domain_events() 

print(f"1. Original (ID: {cat_original.id}) | Ativo: {cat_original.is_active}")


data_dict = cat_original.to_dict()
print(f"2. Serializado (Class: {data_dict.get('class_name')})")

cat_reconstruida = Category.from_dict(data_dict)

print(f"3. Reconstruída (ID: {cat_reconstruida.id}) | Ativo: {cat_reconstruida.is_active}") 
print(f"4. Os objetos são equivalentes? {cat_original == cat_reconstruida}")
print("-" * 50)

print("--- TESTE 2: Eventos de Domínio no Ciclo de Vida ---")

cat_eventos = Category(name="Finanças", is_active=False)
print(f"Categoria criada: {cat_eventos.name}. Ativa: {cat_eventos.is_active}")


cat_eventos.update(name="Investimentos", description="Ações e Fundos")
print(f"-> Update: {cat_eventos.name}")

cat_eventos.activate()
print(f"-> Ativar. Ativa: {cat_eventos.is_active}")

cat_eventos.deactivate()
print(f"-> Desativar. Ativa: {cat_eventos.is_active}")

print("\nLista Final de Eventos Disparados e Limpos (4 eventos esperados):")
for event in cat_eventos.clear_domain_events():
    print(f" -> {event.__class__.__name__} | ID: {event.category_id}")