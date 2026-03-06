CREATE OR REPLACE FUNCTION create_user(
    p_username VARCHAR,
    p_email VARCHAR,
    p_password_hash VARCHAR,
    p_bio TEXT DEFAULT NULL,
    p_avatar_url VARCHAR DEFAULT NULL,
    p_role VARCHAR DEFAULT 'user'
) RETURNS users AS $$
DECLARE
    new_user users%ROWTYPE;
BEGIN
    INSERT INTO users (username, email, password_hash, bio, avatar_url, role)
    VALUES (p_username, p_email, p_password_hash, p_bio, p_avatar_url, p_role)
    RETURNING * INTO new_user;
    
    RETURN new_user;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_user(p_user_id BIGINT)
RETURNS users AS $$
DECLARE
    user_record users%ROWTYPE;
BEGIN
    SELECT * INTO user_record FROM users WHERE id = p_user_id;
    
    IF NOT FOUND THEN
        RETURN NULL;
    END IF;
    
    RETURN user_record;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_user_by_email(p_email VARCHAR)
RETURNS users AS $$
DECLARE
    user_record users%ROWTYPE;
BEGIN
    SELECT * INTO user_record FROM users WHERE email = p_email;
    
    IF NOT FOUND THEN
        RETURN NULL;
    END IF;
    
    RETURN user_record;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_user(
    p_user_id BIGINT,
    p_username VARCHAR DEFAULT NULL,
    p_bio TEXT DEFAULT NULL,
    p_avatar_url VARCHAR DEFAULT NULL,
    p_role VARCHAR DEFAULT NULL
) RETURNS users AS $$
DECLARE
    updated_user users%ROWTYPE;
BEGIN
    UPDATE users SET
        username = COALESCE(p_username, username),
        bio = COALESCE(p_bio, bio),
        avatar_url = COALESCE(p_avatar_url, avatar_url),
        role = COALESCE(p_role, role),
        updated_at = NOW()
    WHERE id = p_user_id
    RETURNING * INTO updated_user;
    
    RETURN updated_user;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_user(p_user_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM users WHERE id = p_user_id;
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_post(
    p_slug VARCHAR,
    p_title VARCHAR,
    p_content TEXT,
    p_user_id BIGINT,
    p_excerpt VARCHAR DEFAULT NULL,
    p_status VARCHAR DEFAULT 'draft',
    p_is_featured BOOLEAN DEFAULT FALSE,
    p_published_at TIMESTAMPTZ DEFAULT NULL
) RETURNS posts AS $$
DECLARE
    new_post posts%ROWTYPE;
    v_published_at TIMESTAMPTZ;
BEGIN
    v_published_at := CASE 
        WHEN p_status = 'published' AND p_published_at IS NULL THEN NOW()
        ELSE p_published_at
    END;
    
    INSERT INTO posts (
        slug, title, content, user_id, excerpt, 
        status, is_featured, published_at
    ) VALUES (
        p_slug, p_title, p_content, p_user_id, p_excerpt,
        p_status, p_is_featured, v_published_at
    ) RETURNING * INTO new_post;
    
    RETURN new_post;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_post(p_post_id BIGINT)
RETURNS posts AS $$
DECLARE
    post_record posts%ROWTYPE;
BEGIN
    SELECT * INTO post_record FROM posts WHERE id = p_post_id;
    RETURN post_record;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_post_by_slug(p_slug VARCHAR)
RETURNS posts AS $$
DECLARE
    post_record posts%ROWTYPE;
BEGIN
    SELECT * INTO post_record FROM posts WHERE slug = p_slug;
    RETURN post_record;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_post(
    p_post_id BIGINT,
    p_title VARCHAR DEFAULT NULL,
    p_content TEXT DEFAULT NULL,
    p_excerpt VARCHAR DEFAULT NULL,
    p_status VARCHAR DEFAULT NULL,
    p_is_featured BOOLEAN DEFAULT NULL
) RETURNS posts AS $$
DECLARE
    updated_post posts%ROWTYPE;
    v_published_at TIMESTAMPTZ;
BEGIN
    IF p_status = 'published' THEN
        SELECT published_at INTO v_published_at FROM posts WHERE id = p_post_id;
        IF v_published_at IS NULL THEN
            v_published_at := NOW();
        ELSE
            v_published_at := NULL;
        END IF;
    END IF;
    
    UPDATE posts SET
        title = COALESCE(p_title, title),
        content = COALESCE(p_content, content),
        excerpt = COALESCE(p_excerpt, excerpt),
        status = COALESCE(p_status, status),
        is_featured = COALESCE(p_is_featured, is_featured),
        published_at = COALESCE(v_published_at, published_at),
        updated_at = NOW()
    WHERE id = p_post_id
    RETURNING * INTO updated_post;
    
    RETURN updated_post;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_post(p_post_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM posts WHERE id = p_post_id;
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION create_category(
    p_name VARCHAR,
    p_slug VARCHAR,
    p_description TEXT DEFAULT NULL,
    p_parent_id BIGINT DEFAULT NULL,
    p_sort_order INTEGER DEFAULT 0
) RETURNS categories AS $$
DECLARE
    new_category categories%ROWTYPE;
BEGIN
    INSERT INTO categories (name, slug, description, parent_id, sort_order)
    VALUES (p_name, p_slug, p_description, p_parent_id, p_sort_order)
    RETURNING * INTO new_category;
    
    RETURN new_category;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_category(p_category_id BIGINT)
RETURNS categories AS $$
DECLARE
    category_record categories%ROWTYPE;
BEGIN
    SELECT * INTO category_record FROM categories WHERE id = p_category_id;
    RETURN category_record;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_category_with_children(p_category_id BIGINT)
RETURNS TABLE(
    id BIGINT,
    name VARCHAR,
    slug VARCHAR,
    description TEXT,
    parent_id BIGINT,
    sort_order INTEGER,
    children JSON
) AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE category_tree AS (
        SELECT *, 1 as level, jsonb_build_array() as children
        FROM categories 
        WHERE id = p_category_id
        
        UNION ALL
        
        SELECT c.*, ct.level + 1, jsonb_build_array()
        FROM categories c
        INNER JOIN category_tree ct ON c.parent_id = ct.id
        WHERE c.id != p_category_id
    )
    SELECT 
        ct.id,
        ct.name,
        ct.slug,
        ct.description,
        ct.parent_id,
        ct.sort_order,
        COALESCE(
            (SELECT jsonb_agg(
                jsonb_build_object(
                    'id', c2.id,
                    'name', c2.name,
                    'slug', c2.slug
                )
             ) FROM categories c2 WHERE c2.parent_id = ct.id),
            '[]'::jsonb
        )::JSON as children
    FROM category_tree ct
    WHERE ct.id = p_category_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_category(
    p_category_id BIGINT,
    p_name VARCHAR DEFAULT NULL,
    p_description TEXT DEFAULT NULL,
    p_parent_id BIGINT DEFAULT NULL,
    p_sort_order INTEGER DEFAULT NULL
) RETURNS categories AS $$
DECLARE
    updated_category categories%ROWTYPE;
BEGIN
    UPDATE categories SET
        name = COALESCE(p_name, name),
        description = COALESCE(p_description, description),
        parent_id = COALESCE(p_parent_id, parent_id),
        sort_order = COALESCE(p_sort_order, sort_order)
    WHERE id = p_category_id
    RETURNING * INTO updated_category;
    
    RETURN updated_category;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_category(p_category_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM categories WHERE id = p_category_id;
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_tag(
    p_name VARCHAR,
    p_slug VARCHAR
) RETURNS tags AS $$
DECLARE
    new_tag tags%ROWTYPE;
BEGIN
    INSERT INTO tags (name, slug) VALUES (p_name, p_slug)
    RETURNING * INTO new_tag;
    
    RETURN new_tag;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_tag(p_tag_id BIGINT)
RETURNS tags AS $$
DECLARE
    tag_record tags%ROWTYPE;
BEGIN
    SELECT * INTO tag_record FROM tags WHERE id = p_tag_id;
    RETURN tag_record;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_tag_by_slug(p_slug VARCHAR)
RETURNS tags AS $$
DECLARE
    tag_record tags%ROWTYPE;
BEGIN
    SELECT * INTO tag_record FROM tags WHERE slug = p_slug;
    RETURN tag_record;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_tag(
    p_tag_id BIGINT,
    p_name VARCHAR DEFAULT NULL,
    p_slug VARCHAR DEFAULT NULL
) RETURNS tags AS $$
DECLARE
    updated_tag tags%ROWTYPE;
BEGIN
    UPDATE tags SET
        name = COALESCE(p_name, name),
        slug = COALESCE(p_slug, slug)
    WHERE id = p_tag_id
    RETURNING * INTO updated_tag;
    
    RETURN updated_tag;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_tag(p_tag_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM tags WHERE id = p_tag_id;
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION assign_tag_to_post(
    p_post_id BIGINT,
    p_tag_id BIGINT
) RETURNS post_tags AS $$
DECLARE
    new_assignment post_tags%ROWTYPE;
BEGIN
    INSERT INTO post_tags (post_id, tag_id)
    VALUES (p_post_id, p_tag_id)
    RETURNING * INTO new_assignment;
    
    RETURN new_assignment;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_post_tags(p_post_id BIGINT)
RETURNS TABLE(
    tag_id BIGINT,
    tag_name VARCHAR,
    tag_slug VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT t.id, t.name, t.slug
    FROM tags t
    INNER JOIN post_tags pt ON t.id = pt.tag_id
    WHERE pt.post_id = p_post_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_tag_posts(p_tag_id BIGINT)
RETURNS TABLE(
    post_id BIGINT,
    post_title VARCHAR,
    post_slug VARCHAR,
    published_at TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.title, p.slug, p.published_at
    FROM posts p
    INNER JOIN post_tags pt ON p.id = pt.post_id
    WHERE pt.tag_id = p_tag_id
    ORDER BY p.published_at DESC;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_post_likes(p_post_id BIGINT)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM post_likes WHERE post_id = p_post_id;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_user(8);