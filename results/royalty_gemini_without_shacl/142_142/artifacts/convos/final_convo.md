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
  AssignClass (50ba31a5-d33b-40c0-a667-2f6043a71f54)
 Call ID: 50ba31a5-d33b-40c0-a667-2f6043a71f54
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (fe4e64ae-4374-4543-9f91-334e7c603f71)
 Call ID: fe4e64ae-4374-4543-9f91-334e7c603f71
  Args:
    source: Juan_Carlos_I
    type: :Person
  AssignClass (f3cdeec5-e87d-49c4-9836-8aa4af66ca06)
 Call ID: f3cdeec5-e87d-49c4-9836-8aa4af66ca06
  Args:
    type: :Woman
    source: Sofia
  AssignClass (cdbe56fa-02b5-4450-b656-ec0086cc5644)
 Call ID: cdbe56fa-02b5-4450-b656-ec0086cc5644
  Args:
    source: Sofia
    type: :Person
  AssignClass (99f1fcf0-a481-409f-a037-8084cab40c88)
 Call ID: 99f1fcf0-a481-409f-a037-8084cab40c88
  Args:
    type: :Woman
    source: Cristina
  AssignClass (bf7fb29e-89b7-4b5d-a899-b8c8d76d5c45)
 Call ID: bf7fb29e-89b7-4b5d-a899-b8c8d76d5c45
  Args:
    source: Cristina
    type: :Person
  AssignClass (f7af3ac3-5add-4fa1-b2d2-28afd020a460)
 Call ID: f7af3ac3-5add-4fa1-b2d2-28afd020a460
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (68f60631-da57-4dea-a4a9-980ecf33e695)
 Call ID: 68f60631-da57-4dea-a4a9-980ecf33e695
  Args:
    type: :Person
    source: Felipe_VI
  AssignClass (1369d012-d7f1-485e-b4eb-374ae33e8c02)
 Call ID: 1369d012-d7f1-485e-b4eb-374ae33e8c02
  Args:
    type: :Woman
    source: Elena
  AssignClass (7bfbba32-9385-4bf8-8ea1-1ed206975339)
 Call ID: 7bfbba32-9385-4bf8-8ea1-1ed206975339
  Args:
    source: Elena
    type: :Person
  AssignClass (79192f8c-cccc-477c-a0d4-8b0a836a0acf)
 Call ID: 79192f8c-cccc-477c-a0d4-8b0a836a0acf
  Args:
    type: :Man
    source: Inaki_Urdangarin
  AssignClass (ea91c0d7-5536-45f7-9f1f-4242ebd55fe6)
 Call ID: ea91c0d7-5536-45f7-9f1f-4242ebd55fe6
  Args:
    type: :Person
    source: Inaki_Urdangarin
  AddTriple (d5c9db42-fbcf-4c3f-9f90-819a87ca6130)
 Call ID: d5c9db42-fbcf-4c3f-9f90-819a87ca6130
  Args:
    target: Cristina
    source: Juan_Carlos_I
    relation: :isFatherOf
  AddTriple (bd43b546-af3c-4e6a-bbba-dfb0dc7dac85)
 Call ID: bd43b546-af3c-4e6a-bbba-dfb0dc7dac85
  Args:
    source: Sofia
    relation: :isMotherOf
    target: Cristina
  AddTriple (cc072a63-1fd4-4ba6-80ef-bc230b481790)
 Call ID: cc072a63-1fd4-4ba6-80ef-bc230b481790
  Args:
    target: Elena
    source: Juan_Carlos_I
    relation: :isFatherOf
  AddTriple (af8f0620-403c-499b-b317-243d96808732)
 Call ID: af8f0620-403c-499b-b317-243d96808732
  Args:
    target: Elena
    relation: :isMotherOf
    source: Sofia
  AddTriple (c1d8405c-3fe6-4ee3-b8a3-65a814a13a78)
 Call ID: c1d8405c-3fe6-4ee3-b8a3-65a814a13a78
  Args:
    target: Felipe_VI
    relation: :isFatherOf
    source: Juan_Carlos_I
  AddTriple (d8c8786d-161b-4c05-88f2-3baf1aadb397)
 Call ID: d8c8786d-161b-4c05-88f2-3baf1aadb397
  Args:
    source: Sofia
    relation: :isMotherOf
    target: Felipe_VI
  AddLiteral (305508b2-c91b-4323-9eca-f456d4f6738d)
 Call ID: 305508b2-c91b-4323-9eca-f456d4f6738d
  Args:
    literal_value: 1965
    source: Cristina
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (a19ba31a-5dcd-48f5-bdd0-84fa61f78155)
 Call ID: a19ba31a-5dcd-48f5-bdd0-84fa61f78155
  Args:
    relation: :hasFather
    source: Cristina
    target: Juan_Carlos_I
  AddTriple (c6cd4aa5-9dde-42a0-af12-bfebd2840e9d)
 Call ID: c6cd4aa5-9dde-42a0-af12-bfebd2840e9d
  Args:
    source: Cristina
    relation: :hasMother
    target: Sofia
  Finish (b869e076-1a84-4ebb-b476-3d2a0f922e7b)
 Call ID: b869e076-1a84-4ebb-b476-3d2a0f922e7b
  Args: