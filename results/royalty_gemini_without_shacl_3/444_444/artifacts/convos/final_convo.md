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
Angelica Margherita Edwina Hicks (born 16 September 1992) is a British fashion illustrator and internet personality.
As the great-granddaughter of Louis Mountbatten, 1st Earl Mountbatten of Burma, she is a relative of the British royal family and is included in the line of succession to the British throne.
Early life and family

Hicks was born on 16 September 1992 to Marina Allegra Federica Silvia Tondato, an Italian designer, and Ashley Louis David Hicks, a British artist and interior designer.
Hicks' paternal grandparents were the English interior decorator and designer David Nightingale Hicks and Lady Pamela Mountbatten, who served as a bridesmaid and as a lady-in-waiting to Elizabeth II.
Through her grandmother, Hicks is a relative of the Mountbatten family, itself a branch of the German princely Battenberg family, and a relative of the British royal family.
Hicks' great-grandparents, Louis Mountbatten, 1st Earl Mountbatten of Burma and The Honourable Edwina Ashley, served as the Viceroy and Vicereine of India.
She is a great-great-granddaughter of Prince Louis of Battenberg (later the 1st Marquess of Milford Haven) and Princess Victoria of Hesse and by Rhine, a granddaughter of Queen Victoria.
Hicks grew up in Chelsea, London and was educated at a boarding school.
Career

Hicks works as a visual artist and fashion illustrator.
Hicks also made commissioned pieces for the American fashion designer Tory Burch and illustrated for the magazines Elle and Porter.
In 2021, Hicks launched a TikTok channel where she parodies haute couture outfits from red carpet events and fashion shows, recreating them out of duct tape, trash bags, metallic wrappers, foil, candy, and other materials.
Her recreations included a Louis Vuitton tank dress worn by Emma Corrin on the cover of Vogue, which she made out of multigrain crackers, a Maison Schiaparelli couture cape that she made out of a white mattress cover, and Cagole boots by Balenciaga that she made out of duct tape.
By July 2022, Hicks amassed over 48,000 followers and her videos collectively received over 4 million likes.
Her videos led to Hicks collaborating with Valentino and Vogue Italia.
By September 2022, Hicks had over 86,000 followers on TikTok.
Personal life

Hicks resides in Carroll Gardens in Brooklyn, New York.



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
  AssignClass (628523fe-7e8f-488e-a7e1-0f6b2d90bcb6)
 Call ID: 628523fe-7e8f-488e-a7e1-0f6b2d90bcb6
  Args:
    type: :Woman
    source: Angelica_Margherita_Edwina_Hicks
  AddLiteral (e350576d-d83e-4fff-babc-702ce3253fc4)
 Call ID: e350576d-d83e-4fff-babc-702ce3253fc4
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Angelica_Margherita_Edwina_Hicks
    literal_value: 1992
  AssignClass (fbf9ba7a-927c-4582-be6e-cded38dd60a6)
 Call ID: fbf9ba7a-927c-4582-be6e-cded38dd60a6
  Args:
    source: Marina_Allegra_Federica_Silvia_Tondato
    type: :Woman
  AssignClass (4f5bc54c-fed3-4658-90a8-5780db7954e7)
 Call ID: 4f5bc54c-fed3-4658-90a8-5780db7954e7
  Args:
    type: :Man
    source: Ashley_Louis_David_Hicks
  AddTriple (e5badddf-d342-47f4-8b0d-861bb19206e5)
 Call ID: e5badddf-d342-47f4-8b0d-861bb19206e5
  Args:
    target: Marina_Allegra_Federica_Silvia_Tondato
    source: Angelica_Margherita_Edwina_Hicks
    relation: :hasMother
  AddTriple (1d97101f-5e8f-431d-9d49-0ad8daed2673)
 Call ID: 1d97101f-5e8f-431d-9d49-0ad8daed2673
  Args:
    target: Ashley_Louis_David_Hicks
    source: Angelica_Margherita_Edwina_Hicks
    relation: :hasFather
  AssignClass (1dd3b55e-978a-41ab-84d2-d8d5b000ae65)
 Call ID: 1dd3b55e-978a-41ab-84d2-d8d5b000ae65
  Args:
    source: David_Nightingale_Hicks
    type: :Man
  AssignClass (99d05f40-751b-468a-a66d-f75c030cf8c1)
 Call ID: 99d05f40-751b-468a-a66d-f75c030cf8c1
  Args:
    type: :Woman
    source: Lady_Pamela_Mountbatten
  AddTriple (9e0fbac2-dd8e-4815-96cd-4daba4073e97)
 Call ID: 9e0fbac2-dd8e-4815-96cd-4daba4073e97
  Args:
    source: Ashley_Louis_David_Hicks
    relation: :hasFather
    target: David_Nightingale_Hicks
  AddTriple (da15f6ed-af47-4876-809e-7d6af583c9a8)
 Call ID: da15f6ed-af47-4876-809e-7d6af583c9a8
  Args:
    source: Ashley_Louis_David_Hicks
    relation: :hasMother
    target: Lady_Pamela_Mountbatten
  AssignClass (0949ddf1-8fa8-46f9-b422-aa127d890d14)
 Call ID: 0949ddf1-8fa8-46f9-b422-aa127d890d14
  Args:
    type: :Man
    source: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
  AssignClass (c85612e2-a6b6-404c-960f-a1e9e900082f)
 Call ID: c85612e2-a6b6-404c-960f-a1e9e900082f
  Args:
    source: The_Honourable_Edwina_Ashley
    type: :Woman
  AddTriple (7c00a0f2-9f67-4156-b53c-bcf8cd1fb124)
 Call ID: 7c00a0f2-9f67-4156-b53c-bcf8cd1fb124
  Args:
    target: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
    relation: :hasFather
    source: Lady_Pamela_Mountbatten
  AddTriple (f01f8fe0-075d-49a1-a298-6604ece31e5f)
 Call ID: f01f8fe0-075d-49a1-a298-6604ece31e5f
  Args:
    source: Lady_Pamela_Mountbatten
    relation: :hasMother
    target: The_Honourable_Edwina_Ashley
  AssignClass (a86f310b-3775-4f10-901e-c33cfe565375)
 Call ID: a86f310b-3775-4f10-901e-c33cfe565375
  Args:
    type: :Man
    source: Prince_Louis_of_Battenberg
  AssignClass (8d3d0dea-00c4-4fa0-bcb5-ecfa92beba3b)
 Call ID: 8d3d0dea-00c4-4fa0-bcb5-ecfa92beba3b
  Args:
    type: :Woman
    source: Princess_Victoria_of_Hesse_and_by_Rhine
  AssignClass (bb5f4f35-06b9-4b53-83ee-310918dcc101)
 Call ID: bb5f4f35-06b9-4b53-83ee-310918dcc101
  Args:
    type: :Woman
    source: Queen_Victoria
  AddTriple (50dfc02f-15a5-47db-af30-918244ce3f65)
 Call ID: 50dfc02f-15a5-47db-af30-918244ce3f65
  Args:
    source: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
    relation: :hasFather
    target: Prince_Louis_of_Battenberg
  AddTriple (ca788bd2-6839-4ae4-bdb8-e59ea7eebed4)
 Call ID: ca788bd2-6839-4ae4-bdb8-e59ea7eebed4
  Args:
    relation: :hasMother
    source: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
    target: Princess_Victoria_of_Hesse_and_by_Rhine
  AddTriple (a46cd441-5c83-40e2-8b27-902a71a7e7b6)
 Call ID: a46cd441-5c83-40e2-8b27-902a71a7e7b6
  Args:
    target: Queen_Victoria
    source: Princess_Victoria_of_Hesse_and_by_Rhine
    relation: :hasMother
  Finish (49185f77-2908-4bef-aa7b-944fc62a235d)
 Call ID: 49185f77-2908-4bef-aa7b-944fc62a235d
  Args: