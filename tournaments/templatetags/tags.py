from django import template

register = template.Library()

@register.simple_tag()
def round_score(score, round):
    if score == 0:
        return 0
    return score
