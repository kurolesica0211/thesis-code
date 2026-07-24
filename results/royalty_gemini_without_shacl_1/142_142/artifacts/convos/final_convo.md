================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
King Juan Carlos IQueen Sofía


The Duchess of Soria and HernaniThe Duke of Soria and Hernani


The Dowager Duchess of Calabria


Infanta Cristina (Cristina Federica Victoria Antonia de la Santísima Trinidad de Borbón y de Grecia, born 13 June 1965) is the younger daughter of King Juan Carlos I and his wife, Queen Sofía.
She is sixth in the line of succession to the Spanish throne, after her brother King Felipe VI's children, her sister Infanta Elena, Duchess of Lugo, and Elena's children Felipe and Victoria.
On 26 September 1997, on the occasion of her marriage to handball player Iñaki Urdangarin, she was created Duchess of Palma de Mallorca by her father, King Juan Carlos.
Cristina represented the Crown during the reign of her father.
Early life

Cristina de Borbón was born on 13 June 1965 at Our Lady of Loreto Sanatorium, now known as ORPEA Madrid Loreto in Madrid and was baptized into the Church at the Palacio de La Zarzuela by the Archbishop of Madrid.
Her godparents were Alfonso, Duke of Anjou and Cádiz (her first cousin once removed), and Infanta Maria Cristina (great-aunt).
Marriage and children

Cristina married team handball player Iñaki Urdangarin at Barcelona Cathedral on 4 October 1997.
On this occasion, she was created Duchess of Palma de Mallorca for life.
On 24 January 2022, Cristina and Urdangarin announced their separation.
Activities and personal work

Cristina started to attend official events at a very young age.
Since finishing her most basic education in 1983, Cristina, along with her sister Elena, supported their parents representing the Crown at official events such as the National Day, the wedding of Princess Astrid of Belgium, the re-burial of Queen Victoria Eugenia at El Escorial, and the state visit of Mexican president Miguel de la Madrid to Spain, among others.
After the corruption scandal of her husband, the Duchess and her husband distanced themselves from the royal family, their last official event was on 12 October 2011.
Regarding her personal work, Cristina has been working for La Caixa Foundation since October 1993.
In April 2013, Infanta Cristina was formally named as a suspect in the case by the judge in charge.
The infanta made her first appearance in the Majorca Court on 8 February 2014, where she denied any knowledge of her husband's dealings.
Spanish judge Jose Castro formalised charges against Infanta Cristina on 25 June 2014.
On 22 December 2014 the High Court of the Balearic Islands announced that Infanta Cristina, her husband, and 15 others would stand trial on tax fraud charges "as soon as next year".
On 12 June 2015, King Felipe VI officially deprived his sister of her dukedom, privately announcing his intention beforehand.
After this decision was made public, Cristina's lawyer, Miquel Roca, declared that the king's decision followed a formal request from the infanta, although the Royal Household denied it, saying that her renunciation to the title was after the king's private phone call to communicate her the decision.
Her right of succession to the throne, and to the royal title of infanta were unaffected.
Cristina's trial began on 11 January 2016, presided over by three judges in Palma de Mallorca.
Titles, styles, honours and arms

Titles and styles

As a child of a Spanish monarch, Cristina is entitled to the designation and rank of infanta (princess) with the style of Royal Highness.
On the occasion of her marriage in 1997, she was created Duchess of Palma de Mallorca.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (58aa72bc-c4c0-44bc-9a92-d90a6418aed5)
 Call ID: 58aa72bc-c4c0-44bc-9a92-d90a6418aed5
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (de45702e-fe59-4ebb-94a4-be016383acc5)
 Call ID: de45702e-fe59-4ebb-94a4-be016383acc5
  Args:
    type: :Person
    source: Juan_Carlos_I
  AssignClass (3a0cd2d1-5330-4fe0-8140-01476da6dc55)
 Call ID: 3a0cd2d1-5330-4fe0-8140-01476da6dc55
  Args:
    type: :Woman
    source: Sofia
  AssignClass (1a754f0d-ff8d-421b-9280-b3207f6a4a32)
 Call ID: 1a754f0d-ff8d-421b-9280-b3207f6a4a32
  Args:
    type: :Person
    source: Sofia
  AssignClass (39b839b2-f2ff-4d6e-b0fa-dab66cddc159)
 Call ID: 39b839b2-f2ff-4d6e-b0fa-dab66cddc159
  Args:
    type: :Woman
    source: Cristina
  AssignClass (e75d6b8f-afe4-47f5-b21b-7eceba1960f0)
 Call ID: e75d6b8f-afe4-47f5-b21b-7eceba1960f0
  Args:
    type: :Person
    source: Cristina
  AssignClass (4129e02a-fd3e-41cb-bd6d-8bbc418e1f96)
 Call ID: 4129e02a-fd3e-41cb-bd6d-8bbc418e1f96
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (c471347d-ada1-4172-be58-ce563feffb28)
 Call ID: c471347d-ada1-4172-be58-ce563feffb28
  Args:
    type: :Person
    source: Felipe_VI
  AssignClass (75cad38a-7e34-49d2-9a0b-d71a2bf4100c)
 Call ID: 75cad38a-7e34-49d2-9a0b-d71a2bf4100c
  Args:
    type: :Woman
    source: Elena
  AssignClass (7c924876-582f-471b-97b6-f80a4f08c1f7)
 Call ID: 7c924876-582f-471b-97b6-f80a4f08c1f7
  Args:
    type: :Person
    source: Elena
  AssignClass (b56a0f87-9e15-459b-83ab-fd5aa1f31fbf)
 Call ID: b56a0f87-9e15-459b-83ab-fd5aa1f31fbf
  Args:
    type: :Man
    source: Inaki_Urdangarin
  AssignClass (472bc9e3-5c8b-4d75-adae-6d0162227872)
 Call ID: 472bc9e3-5c8b-4d75-adae-6d0162227872
  Args:
    type: :Person
    source: Inaki_Urdangarin
  AddTriple (ec9480ac-558d-444c-8ffe-09ac90cc5348)
 Call ID: ec9480ac-558d-444c-8ffe-09ac90cc5348
  Args:
    source: Cristina
    target: Juan_Carlos_I
    relation: :hasFather
  AddTriple (13a6f757-2c5c-4e9f-9219-572ba195b350)
 Call ID: 13a6f757-2c5c-4e9f-9219-572ba195b350
  Args:
    source: Cristina
    relation: :hasMother
    target: Sofia
  AddTriple (0a8856bf-530d-445e-8eca-2d43ab385e11)
 Call ID: 0a8856bf-530d-445e-8eca-2d43ab385e11
  Args:
    relation: :hasFather
    target: Juan_Carlos_I
    source: Elena
  AddTriple (1f90c0b9-1aed-432b-abdb-34047a214662)
 Call ID: 1f90c0b9-1aed-432b-abdb-34047a214662
  Args:
    relation: :hasMother
    target: Sofia
    source: Elena
  AddTriple (829530a4-72be-47f0-aedc-8fdbd6f74bef)
 Call ID: 829530a4-72be-47f0-aedc-8fdbd6f74bef
  Args:
    source: Felipe_VI
    relation: :hasFather
    target: Juan_Carlos_I
  AddTriple (7efc9e5e-39c1-4e0c-8d11-37e10833c9e8)
 Call ID: 7efc9e5e-39c1-4e0c-8d11-37e10833c9e8
  Args:
    source: Felipe_VI
    relation: :hasMother
    target: Sofia
  AddLiteral (55e7fb8c-ece5-4cdf-b158-814714bec9e8)
 Call ID: 55e7fb8c-ece5-4cdf-b158-814714bec9e8
  Args:
    source: Cristina
    literal_type: xsd:integer
    literal_value: 1965
    relation: :hasBirthYear
  AddLiteral (8f33e320-cb0b-4c2e-9f8d-ac0d171cdf63)
 Call ID: 8f33e320-cb0b-4c2e-9f8d-ac0d171cdf63
  Args:
    literal_type: xsd:string
    source: Cristina
    relation: :knownAs
    literal_value: Cristina Federica Victoria Antonia de la Santísima Trinidad de Borbón y de Grecia
  AddTriple (56ff038a-3629-48da-8627-0ac0e10c1fdf)
 Call ID: 56ff038a-3629-48da-8627-0ac0e10c1fdf
  Args:
    target: Inaki_Urdangarin
    relation: :hasMarriageYear
    source: Cristina
  AddLiteral (97c3acfa-7379-4a5c-af35-f8b5a21553df)
 Call ID: 97c3acfa-7379-4a5c-af35-f8b5a21553df
  Args:
    literal_value: 1997
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Cristina
  Finish (f8436814-8ab9-44f8-99fa-d7c764bcb178)
 Call ID: f8436814-8ab9-44f8-99fa-d7c764bcb178
  Args: