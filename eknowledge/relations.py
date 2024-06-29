RELATIONS = [
    'is_a',     # Subclass relationship
    'part_of',  # Compositional relationship
    'has_part', # Reverse of part_of
    'associated_with',  # General association
    'equivalent_to',    # Equivalence relationship
    'disjoint_with',    # Disjoint relationship
    'depends_on',       # Dependency relationship
    'inverse_of',       # Inverse relationship
    'transitive',       # Transitive relationship
    'symmetrical',      # Symmetrical relationship
    'asymmetrical',     # Asymmetrical relationship
    'reflexive',        # Reflexive relationship
    'has_property',     # Entity has a specific property
    'has_attribute',    # Similar to has_property, more general
    'connected_to',     # General connection, less specific than associated_with
    'used_for',         # Indicates typical use or purpose
    'belongs_to',       # Membership relation
    'contains',         # Contains relationship
    'produced_by',      # Indicates production or creation relationship
    'preceded_by',      # Temporal or sequential precedence
    'succeeded_by',     # Temporal or sequential succession
    'interacts_with',   # Interaction without specific direction
    'causes',           # Causality relationship
    'influences',       # Influence, weaker than causality
    'contradicts',      # Contradictory relationship
    'complementary_to', # Complementarity in properties or function
    'alternative_to',   # Provides an alternative to
    'derived_from',     # Indicates origin or derivation
    'has_member',       # Indicates membership (group to individual)
    'member_of',        # Individual is member of group (reverse of has_member)
    'subclass_of',      # Another form of is_a, commonly used in RDF/OWL
    'superclass_of',    # Reverse of subclass_of
    'annotated_with',   # Used for linking annotations or metadata
    'realizes',         # Realization relationship in BFO (Basic Formal Ontology)
    'has_quality',      # Quality possession
    'located_in',       # Spatial containment or location relationship
    'contains_information_about',  # Information content relationship
    'expresses',        # Expression relationship in genetics or traits
    'enabled_by',       # Enabling condition relationship
    'occurs_in',        # Temporal occurrence within a context
    'during',           # Temporal relationship specifying during another event
    'has_function',     # Functionality relationship
    'has_role',         # Role specification relationship
    'has_participant',  # Participation in an event or process
    'has_agent',        # Agency relationship
    'has_output',       # Output specification relationship
    'has_input',        # Input specification relationship
    'measured_by',      # Measurement relationship
    'provides',         # Provision relationship
    'requires',         # Requirement relationship
    'temporally_related_to',    # General temporal relationship
    'spatially_related_to',     # General spatial relationship
    'has_version',      # Version control relationship
    'has_exception',    # Exception specification
    'aggregates',       # Aggregation relationship
    'decomposed_into',  # Decomposition relationship
    'reified_as',       # Reification relationship
    'instantiated_by',  # Instantiation relationship
    'has_potential',    # Potentiality relationship
    'has_motive',       # Motivation relationship
    'negatively_regulates',  # Negative regulation in biological contexts
    'positively_regulates',  # Positive regulation in biological contexts
    'has_symptom',      # Symptomatic relationship in medical ontologies
    'treated_by',       # Treatment relationship in medical contexts
    'diagnosed_by'      # Diagnostic relationship in medical contexts
]