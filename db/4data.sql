TRUNCATE users, posts, categories, tags, post_categories, post_tags, post_views, post_likes RESTART IDENTITY CASCADE;

-- Пользователи
INSERT INTO users (username, email, password_hash, role, bio) VALUES
('alice_dev', 'alice@example.com', 'hash_alice_123', 'admin', 'Senior Developer и автор блога'),
('bob_coder', 'bob@example.com', 'hash_bob_456', 'editor', 'Люблю писать о программировании'),
('charlie_blogger', 'charlie@example.com', 'hash_charlie_789', 'user', 'Начинающий блогер');

-- Категории
INSERT INTO categories (name, slug, description) VALUES
('Программирование', 'programming', 'Всё о разработке ПО'),
('Базы данных', 'databases', 'PostgreSQL, Redis, MongoDB'),
('DevOps', 'devops', 'CI/CD, Docker, Kubernetes');

-- Теги
INSERT INTO tags (name, slug) VALUES
('postgresql', 'postgresql'),
('redis', 'redis'),
('docker', 'docker'),
('sql', 'sql'),
('nosql', 'nosql'),
('api', 'api');

-- Посты
INSERT INTO posts (slug, title, content, excerpt, user_id, status, views_count) VALUES
('postgresql-vs-redis-caching', 'PostgreSQL vs Redis: Сравнение для кеширования', 
'Подробное сравнение двух технологий...', 'Что выбрать для кеширования?', 1, 'published', 1500),
('docker-compose-guide', 'Полное руководство по Docker Compose', 
'Как оркестрировать контейнеры...', 'Учимся управлять многоконтейнерными приложениями', 2, 'published', 2300),
('sql-optimization-tips', '10 советов по оптимизации SQL запросов', 
'Как ускорить ваши запросы...', 'Практические советы по оптимизации', 1, 'draft', 0);

-- Связи
INSERT INTO post_categories (post_id, category_id) VALUES
(1, 2), (2, 3), (3, 1), (3, 2);

INSERT INTO post_tags (post_id, tag_id) VALUES
(1, 1), (1, 2), (1, 5), (2, 3), (3, 1), (3, 4);

-- Просмотры
INSERT INTO post_views (post_id, viewer_ip, viewed_at) VALUES
(1, '192.168.1.1', NOW() - INTERVAL '1 hour'),
(1, '192.168.1.2', NOW() - INTERVAL '30 minutes'),
(2, '192.168.1.1', NOW() - INTERVAL '2 hours'),
(2, '192.168.1.3', NOW() - INTERVAL '1 hour'),
(2, '192.168.1.4', NOW() - INTERVAL '15 minutes');

-- Обновляем счетчики
UPDATE posts SET views_count = (
    SELECT COUNT(*) FROM post_views WHERE post_id = posts.id
);