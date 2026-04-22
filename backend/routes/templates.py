from flask import Blueprint, request, jsonify
from models.database import PromptTemplate

templates_bp = Blueprint('templates', __name__)

@templates_bp.route('/templates', methods=['GET'])
def list_templates():
    """List all built-in templates, optionally filtered by category/technique."""
    category = request.args.get('category', '')
    technique = request.args.get('technique', '')

    query = PromptTemplate.query.filter_by(is_builtin=True)
    if category:
        query = query.filter_by(category=category)
    if technique:
        query = query.filter_by(technique=technique)

    templates = query.all()
    categories = {}
    for t in templates:
        cat = t.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(t.to_dict())

    return jsonify({
        'templates': [t.to_dict() for t in templates],
        'by_category': categories,
        'total': len(templates)
    }), 200


@templates_bp.route('/templates/<int:template_id>', methods=['GET'])
def get_template(template_id):
    """Get a specific built-in template with full details."""
    template = PromptTemplate.query.filter_by(id=template_id, is_builtin=True).first_or_404()
    return jsonify(template.to_dict()), 200