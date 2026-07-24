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
Thomas Patrick John Anson, 5th Earl of Lichfield (25 April 1939 – 11 November 2005), was an English photographer from the Anson family.
He inherited the Earldom of Lichfield in 1960 from his paternal grandfather.
In his professional practice he was known as Patrick Lichfield.
Biography

Thomas Patrick John Anson was born on 25 April 1939.
He was the only son of Lieutenant-Colonel Thomas William Arnold Anson, Viscount Anson (1913–1958), the eldest son and heir apparent of Thomas Edward Anson, 4th Earl of Lichfield (1883–1960).
His mother was born Anne Bowes-Lyon (1917–1980), a niece of Queen Elizabeth the Queen Mother.
His parents divorced in 1948, and his mother subsequently became Princess Anne of Denmark after her remarriage to Prince Georg of Denmark in 1950.
He had one sister, Lady Elizabeth Georgiana Anson (1941–2020), who married Sir Geoffrey Adam Shakerley, 6th Baronet.
Lichfield was educated at two boarding independent schools: Wellesley House School in the coastal town of Broadstairs in Kent, and Harrow School in Harrow on the Hill in north-west London, followed by the Royal Military Academy Sandhurst.
His father died in 1958, leaving Patrick to succeed as 5th Earl of Lichfield when his grandfather died in 1960.
Lichfield joined the Grenadier Guards in 1959.
He was selected to take the official photographs of the wedding of the Prince and Princess of Wales in 1981, and subsequently became one of the UK's best-known photographers.
He was chosen by Queen Elizabeth II and the Duke of Edinburgh to take official pictures of her Golden Jubilee in 2002.
He also cameoed in the British sitcom Keeping Up Appearances, appearing in the episode "Sea Fever" as a passenger on the Queen Elizabeth 2.
Lichfield resided in an apartment at the former family seat of Shugborough Hall, near Cannock Chase in Staffordshire.
Marriage and children

On 8 March 1975 Lichfield married Lady Leonora Grosvenor, elder daughter of Robert Grosvenor, 5th Duke of Westminster and Hon.
The Countess of Lichfield has not remarried and has retained her title.
She and the Earl had one son and two daughters together:


Lichfield's most recent partner was the biographer Lady Annunziata Asquith, daughter of Julian Asquith, 2nd Earl of Oxford and Asquith.
Death

On 10 November 2005, Lichfield suffered a major stroke and died the following day at the John Radcliffe Hospital in Oxford.
Lichfield's apartment at Shugborough now houses an exhibition of his work, together with a recreation of his studio.



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
  AssignClass (321d42e6-6844-4155-a363-006db2becbbb)
 Call ID: 321d42e6-6844-4155-a363-006db2becbbb
  Args:
    type: :Man
    source: Thomas_Patrick_John_Anson
  AssignClass (c929d0b2-6177-40ee-85a3-63dc78fd956d)
 Call ID: c929d0b2-6177-40ee-85a3-63dc78fd956d
  Args:
    source: Thomas_Patrick_John_Anson
    type: :Person
  AddLiteral (f0e0905c-045e-47bf-b07b-8df7c433bfc5)
 Call ID: f0e0905c-045e-47bf-b07b-8df7c433bfc5
  Args:
    relation: :hasBirthYear
    source: Thomas_Patrick_John_Anson
    literal_value: 1939
    literal_type: xsd:positiveInteger
  AddLiteral (40cbaa20-36b8-4c32-bde8-06ed1047a943)
 Call ID: 40cbaa20-36b8-4c32-bde8-06ed1047a943
  Args:
    literal_value: 2005
    literal_type: xsd:positiveInteger
    source: Thomas_Patrick_John_Anson
    relation: :hasDeathYear
  AddLiteral (dd9bb948-ecda-4091-8edc-d02bb1d1574c)
 Call ID: dd9bb948-ecda-4091-8edc-d02bb1d1574c
  Args:
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Patrick Lichfield
    source: Thomas_Patrick_John_Anson
  AssignClass (f47032cc-df9a-4391-9b1b-3dd6b1d51fc6)
 Call ID: f47032cc-df9a-4391-9b1b-3dd6b1d51fc6
  Args:
    type: :Man
    source: Thomas_William_Arnold_Anson
  AssignClass (9fb306e5-f187-4802-ae7e-3642b6a8e1a9)
 Call ID: 9fb306e5-f187-4802-ae7e-3642b6a8e1a9
  Args:
    type: :Person
    source: Thomas_William_Arnold_Anson
  AddLiteral (601af69a-4539-4ca5-8184-a0503428e12f)
 Call ID: 601af69a-4539-4ca5-8184-a0503428e12f
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1913
    source: Thomas_William_Arnold_Anson
    relation: :hasBirthYear
  AddLiteral (f6088009-8234-4314-b06b-ff6e29fc8926)
 Call ID: f6088009-8234-4314-b06b-ff6e29fc8926
  Args:
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
    literal_value: 1958
    source: Thomas_William_Arnold_Anson
  AddTriple (7c2399e0-fd49-48f5-ad06-4eec237278a6)
 Call ID: 7c2399e0-fd49-48f5-ad06-4eec237278a6
  Args:
    target: Thomas_William_Arnold_Anson
    source: Thomas_Patrick_John_Anson
    relation: :hasFather
  AssignClass (6d4bba5e-76d0-4624-9b84-49218103a577)
 Call ID: 6d4bba5e-76d0-4624-9b84-49218103a577
  Args:
    source: Thomas_Edward_Anson
    type: :Man
  AssignClass (e247117d-cc65-403e-ad36-89d557f73080)
 Call ID: e247117d-cc65-403e-ad36-89d557f73080
  Args:
    type: :Person
    source: Thomas_Edward_Anson
  AddLiteral (9f94465d-bfe6-4363-a185-4d1d4a9dc37e)
 Call ID: 9f94465d-bfe6-4363-a185-4d1d4a9dc37e
  Args:
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    literal_value: 1883
    source: Thomas_Edward_Anson
  AddLiteral (6e069a05-ee8e-43e4-9ba5-715b099daf36)
 Call ID: 6e069a05-ee8e-43e4-9ba5-715b099daf36
  Args:
    source: Thomas_Edward_Anson
    literal_value: 1960
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
  AddTriple (47a93aaf-f549-4bb2-bb0b-c5a3b471493d)
 Call ID: 47a93aaf-f549-4bb2-bb0b-c5a3b471493d
  Args:
    target: Thomas_Edward_Anson
    source: Thomas_William_Arnold_Anson
    relation: :hasFather
  AssignClass (b0ecfcbf-89a7-49d0-8324-28eded976b01)
 Call ID: b0ecfcbf-89a7-49d0-8324-28eded976b01
  Args:
    type: :Woman
    source: Anne_Bowes-Lyon
  AssignClass (a5cd4ae8-e237-4906-b7ca-6dfd49a47d8e)
 Call ID: a5cd4ae8-e237-4906-b7ca-6dfd49a47d8e
  Args:
    type: :Person
    source: Anne_Bowes-Lyon
  AddLiteral (dafc2b0b-6511-4d57-b436-1e4cfff9c8d3)
 Call ID: dafc2b0b-6511-4d57-b436-1e4cfff9c8d3
  Args:
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    literal_value: 1917
    source: Anne_Bowes-Lyon
  AddLiteral (08d91de0-0186-4f6b-9dcc-fb09d58ac547)
 Call ID: 08d91de0-0186-4f6b-9dcc-fb09d58ac547
  Args:
    relation: :hasDeathYear
    literal_value: 1980
    literal_type: xsd:positiveInteger
    source: Anne_Bowes-Lyon
  AddTriple (a110649f-21b5-4554-9963-38a65d6dbd5f)
 Call ID: a110649f-21b5-4554-9963-38a65d6dbd5f
  Args:
    source: Thomas_Patrick_John_Anson
    relation: :hasMother
    target: Anne_Bowes-Lyon
  AssignClass (07f6474b-a411-4f31-9fab-2a8ae4d38778)
 Call ID: 07f6474b-a411-4f31-9fab-2a8ae4d38778
  Args:
    source: Lady_Elizabeth_Georgiana_Anson
    type: :Woman
  AssignClass (a5d16c2e-61c3-41d7-9b75-069d0bca7258)
 Call ID: a5d16c2e-61c3-41d7-9b75-069d0bca7258
  Args:
    type: :Person
    source: Lady_Elizabeth_Georgiana_Anson
  AddLiteral (47a189d0-f804-4ba8-99dc-9161e6a36100)
 Call ID: 47a189d0-f804-4ba8-99dc-9161e6a36100
  Args:
    source: Lady_Elizabeth_Georgiana_Anson
    literal_type: xsd:positiveInteger
    literal_value: 1941
    relation: :hasBirthYear
  AddLiteral (4e057b3f-6ac5-44ea-b52f-ab81af838346)
 Call ID: 4e057b3f-6ac5-44ea-b52f-ab81af838346
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 2020
    source: Lady_Elizabeth_Georgiana_Anson
    relation: :hasDeathYear
  AddTriple (38b17eab-c0ad-4e73-ba34-670b2f5d51c0)
 Call ID: 38b17eab-c0ad-4e73-ba34-670b2f5d51c0
  Args:
    target: Lady_Elizabeth_Georgiana_Anson
    relation: :hasSister
    source: Thomas_Patrick_John_Anson
  AddTriple (2e4b9426-389f-4b93-bbe8-8331acaf130c)
 Call ID: 2e4b9426-389f-4b93-bbe8-8331acaf130c
  Args:
    target: Thomas_William_Arnold_Anson
    relation: :hasFather
    source: Lady_Elizabeth_Georgiana_Anson
  AddTriple (4d459ad5-d707-4ebe-b8e5-5c096827ed61)
 Call ID: 4d459ad5-d707-4ebe-b8e5-5c096827ed61
  Args:
    target: Anne_Bowes-Lyon
    relation: :hasMother
    source: Lady_Elizabeth_Georgiana_Anson
  AssignClass (7b586c07-65bf-498a-ae63-00d409e9b522)
 Call ID: 7b586c07-65bf-498a-ae63-00d409e9b522
  Args:
    source: Lady_Leonora_Grosvenor
    type: :Woman
  AssignClass (378babb8-3775-4a6f-a2cc-125b8979b551)
 Call ID: 378babb8-3775-4a6f-a2cc-125b8979b551
  Args:
    source: Lady_Leonora_Grosvenor
    type: :Person
  AddTriple (44559b03-cf15-460d-9a0a-d60ca309cf11)
 Call ID: 44559b03-cf15-460d-9a0a-d60ca309cf11
  Args:
    relation: :hasRelation
    source: Thomas_Patrick_John_Anson
    target: Lady_Leonora_Grosvenor
  AddLiteral (15387c60-2cfd-4172-a7bd-a57f957b8da9)
 Call ID: 15387c60-2cfd-4172-a7bd-a57f957b8da9
  Args:
    relation: :hasMarriageYear
    source: Thomas_Patrick_John_Anson
    literal_type: xsd:positiveInteger
    literal_value: 1975
  AssignClass (f96bfd27-b993-4c62-bffd-f0ad12b0042f)
 Call ID: f96bfd27-b993-4c62-bffd-f0ad12b0042f
  Args:
    source: Robert_Grosvenor
    type: :Man
  AssignClass (514315f4-5a67-469d-8f2c-22ecec47e0fd)
 Call ID: 514315f4-5a67-469d-8f2c-22ecec47e0fd
  Args:
    type: :Person
    source: Robert_Grosvenor
  AddTriple (1bf5e7b7-777b-43a5-b780-b2fe8d186f0d)
 Call ID: 1bf5e7b7-777b-43a5-b780-b2fe8d186f0d
  Args:
    source: Lady_Leonora_Grosvenor
    relation: :hasFather
    target: Robert_Grosvenor
  AssignClass (6f4403b3-877d-4753-ba71-bce643868cbd)
 Call ID: 6f4403b3-877d-4753-ba71-bce643868cbd
  Args:
    source: Lady_Annunziata_Asquith
    type: :Woman
  AssignClass (24148ef3-31bc-45a0-bf99-1295d65ef774)
 Call ID: 24148ef3-31bc-45a0-bf99-1295d65ef774
  Args:
    type: :Person
    source: Lady_Annunziata_Asquith
  AddTriple (78caee1b-e0f8-45ce-8f44-4bf0311d684f)
 Call ID: 78caee1b-e0f8-45ce-8f44-4bf0311d684f
  Args:
    relation: :hasRelation
    source: Thomas_Patrick_John_Anson
    target: Lady_Annunziata_Asquith
  AssignClass (54381087-9ce9-43c2-b1a3-22d5000b5aae)
 Call ID: 54381087-9ce9-43c2-b1a3-22d5000b5aae
  Args:
    source: Julian_Asquith
    type: :Man
  AssignClass (2ac8d90a-93eb-4861-b700-acec61f1b7ec)
 Call ID: 2ac8d90a-93eb-4861-b700-acec61f1b7ec
  Args:
    source: Julian_Asquith
    type: :Person
  AddTriple (e3b4b689-9b45-4a6c-a6e8-0b7ff6a835a1)
 Call ID: e3b4b689-9b45-4a6c-a6e8-0b7ff6a835a1
  Args:
    source: Lady_Annunziata_Asquith
    relation: :hasFather
    target: Julian_Asquith
  Finish (5756899a-f2d9-418f-8acf-b91489cdc2d1)
 Call ID: 5756899a-f2d9-418f-8acf-b91489cdc2d1
  Args: