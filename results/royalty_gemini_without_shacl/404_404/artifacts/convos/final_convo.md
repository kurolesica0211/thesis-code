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
Lord Ivar Alexander Michael Mountbatten, DL (born 9 March 1963) is a British aristocrat, farmer, geologist, businessman, and reality television personality.
Early life and family

Ivar
Alexander Michael Mountbatten was born in London, to David Mountbatten, 3rd Marquess of Milford Haven, and the former Janet Mercedes Bryce.
His elder brother is George Mountbatten, 4th Marquess of Milford Haven.
His paternal grandfather was Prince George of Battenberg, through whom he is a morganatic descendant of the House of Hesse-Darmstadt.
Mountbatten grew up at Moyns Park in Essex.
In a June 2022 interview with Tatler Mountbatten commented on the 1930s Gloria Vanderbilt child custody trial, where a maid made an allegation of a lesbian affair between the child's mother Gloria Morgan Vanderbilt and the Marchioness of Milford Haven, Mountbatten's grandmother.
Mountbatten was educated at Gordonstoun School, the same school attended by Prince Philip and Charles III, and he graduated from Middlebury College in Vermont with a BA degree.
Career

Mountbatten began his career as a geologist and spent significant time working in South America during his early career.
Starting in 1995, Mountbatten began his involvement in business pursuits, including being the director of the UK subsidiary of DMX Music and being involved with Coldharbour Mill Working Wool Museum.
Mountbatten was later involved with SCL Group, the parent company of the now-defunct data analytics firm Cambridge Analytica.
Mountbatten also serves as a Deputy Lieutenant of Devon.
In 2019, Mountbatten began a career in reality television by starring in the sixth series of Treasure Island with Bear Grylls.
In October 2024, Mountbatten was announced to be part of the third season of the American reality competition series The Traitors, which premiered on 9 January 2025.
Personal life

Mountbatten married Penelope Anne Vere Thompson (born Salisbury, Wiltshire, 17 March 1966), only daughter of Colin Graham Thompson of Old Manor House, Sutton Veny, Wiltshire, and Rosemary Vere Edwardes.
In September 2016, Mountbatten revealed that he was in a relationship with James Coyle, an airline cabin services director whom he met while at a ski resort in Verbier.
Mountbatten's former wife walked him down the aisle and 'gave him away' at the suggestion of their daughters.
Mountbatten is a godparent of Lady Louise Windsor (born 2003), the daughter of Prince Edward and Sophie.
Mountbatten inherited Moyns Park in 1992 along with his brother, George Mountbatten, 4th Marquess of Milford Haven, but in 1997 moved to Bridwell Park in Uffculme, Devon.



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
  AssignClass (b3840c62-7880-4af4-9bce-701e888f33ba)
 Call ID: b3840c62-7880-4af4-9bce-701e888f33ba
  Args:
    source: Ivar_Mountbatten
    type: :Man
  AssignClass (23236d40-0ca4-4604-b883-900645896346)
 Call ID: 23236d40-0ca4-4604-b883-900645896346
  Args:
    source: Ivar_Mountbatten
    type: :Person
  AddLiteral (03c7fc8a-7026-4e7b-bdf5-936fd5cc6219)
 Call ID: 03c7fc8a-7026-4e7b-bdf5-936fd5cc6219
  Args:
    relation: :hasBirthYear
    literal_value: 1963
    literal_type: xsd:integer
    source: Ivar_Mountbatten
  AssignClass (477cc2c6-b3ff-4835-afca-c3573a052cdf)
 Call ID: 477cc2c6-b3ff-4835-afca-c3573a052cdf
  Args:
    source: David_Mountbatten
    type: :Man
  AssignClass (2062f0ca-704d-48b1-968f-7feb15dcd871)
 Call ID: 2062f0ca-704d-48b1-968f-7feb15dcd871
  Args:
    source: David_Mountbatten
    type: :Person
  AssignClass (19810071-80f4-4fc8-bf19-fddd86fbb63c)
 Call ID: 19810071-80f4-4fc8-bf19-fddd86fbb63c
  Args:
    type: :Woman
    source: Janet_Mercedes_Bryce
  AssignClass (80b802d0-f3e9-4d1a-838a-adc92ed6839e)
 Call ID: 80b802d0-f3e9-4d1a-838a-adc92ed6839e
  Args:
    source: Janet_Mercedes_Bryce
    type: :Person
  AddTriple (11b49870-0703-491a-88d6-d5e44b3401cf)
 Call ID: 11b49870-0703-491a-88d6-d5e44b3401cf
  Args:
    target: David_Mountbatten
    relation: :hasFather
    source: Ivar_Mountbatten
  AddTriple (201bae99-a99b-4712-9e2d-097fb7d92e6c)
 Call ID: 201bae99-a99b-4712-9e2d-097fb7d92e6c
  Args:
    relation: :hasMother
    target: Janet_Mercedes_Bryce
    source: Ivar_Mountbatten
  AssignClass (14b16c88-7399-4c7f-9893-a7d49c2aed3c)
 Call ID: 14b16c88-7399-4c7f-9893-a7d49c2aed3c
  Args:
    source: George_Mountbatten_4th_Marquess
    type: :Man
  AssignClass (63f8fd2d-cc55-4689-acbf-7d04b6d2e8ac)
 Call ID: 63f8fd2d-cc55-4689-acbf-7d04b6d2e8ac
  Args:
    type: :Person
    source: George_Mountbatten_4th_Marquess
  AddTriple (7f66c24c-ad59-439f-aceb-90670730bb78)
 Call ID: 7f66c24c-ad59-439f-aceb-90670730bb78
  Args:
    target: George_Mountbatten_4th_Marquess
    relation: :hasBrother
    source: Ivar_Mountbatten
  AssignClass (2a3941ae-737f-4619-9d6b-fef11fab4433)
 Call ID: 2a3941ae-737f-4619-9d6b-fef11fab4433
  Args:
    type: :Man
    source: Prince_George_of_Battenberg
  AssignClass (a6044bac-14de-46db-91d3-7e766ac01226)
 Call ID: a6044bac-14de-46db-91d3-7e766ac01226
  Args:
    source: Prince_George_of_Battenberg
    type: :Person
  AddTriple (a704fc7f-bd24-4fb2-9adf-26604d392c61)
 Call ID: a704fc7f-bd24-4fb2-9adf-26604d392c61
  Args:
    relation: :hasFather
    target: Prince_George_of_Battenberg
    source: David_Mountbatten
  AssignClass (6e1df429-0bb3-4a27-87d8-0c05875d5472)
 Call ID: 6e1df429-0bb3-4a27-87d8-0c05875d5472
  Args:
    source: Penelope_Anne_Vere_Thompson
    type: :Woman
  AssignClass (1bbbf2b0-2d96-4099-80c4-da9d94c01c02)
 Call ID: 1bbbf2b0-2d96-4099-80c4-da9d94c01c02
  Args:
    source: Penelope_Anne_Vere_Thompson
    type: :Person
  AddLiteral (4221b917-46fd-4617-9d62-baa2e9cfcdd0)
 Call ID: 4221b917-46fd-4617-9d62-baa2e9cfcdd0
  Args:
    literal_type: xsd:integer
    literal_value: 1966
    relation: :hasBirthYear
    source: Penelope_Anne_Vere_Thompson
  AssignClass (e179fd84-224e-4959-8cdc-1d6d71f13e3b)
 Call ID: e179fd84-224e-4959-8cdc-1d6d71f13e3b
  Args:
    type: :Man
    source: Colin_Graham_Thompson
  AssignClass (945f63e9-c2dd-4468-9f10-db2df4b17eda)
 Call ID: 945f63e9-c2dd-4468-9f10-db2df4b17eda
  Args:
    source: Colin_Graham_Thompson
    type: :Person
  AssignClass (068d27d6-a4b1-4edb-9d43-c2e68aeda221)
 Call ID: 068d27d6-a4b1-4edb-9d43-c2e68aeda221
  Args:
    type: :Woman
    source: Rosemary_Vere_Edwardes
  AssignClass (f88a8753-de29-40bf-b8fd-c369ce09db0a)
 Call ID: f88a8753-de29-40bf-b8fd-c369ce09db0a
  Args:
    source: Rosemary_Vere_Edwardes
    type: :Person
  AddTriple (c49b7748-d73b-4628-9406-0cfa3798311e)
 Call ID: c49b7748-d73b-4628-9406-0cfa3798311e
  Args:
    source: Penelope_Anne_Vere_Thompson
    relation: :hasFather
    target: Colin_Graham_Thompson
  AddTriple (a18c1bce-4d9d-4a6c-84e8-ab18943a648b)
 Call ID: a18c1bce-4d9d-4a6c-84e8-ab18943a648b
  Args:
    relation: :hasMother
    target: Rosemary_Vere_Edwardes
    source: Penelope_Anne_Vere_Thompson
  AssignClass (9540dbe9-0d3d-4136-bd95-1a5143e84ebc)
 Call ID: 9540dbe9-0d3d-4136-bd95-1a5143e84ebc
  Args:
    type: :Man
    source: James_Coyle
  AssignClass (d232cb1c-d965-47fc-bd8b-0a91742d179d)
 Call ID: d232cb1c-d965-47fc-bd8b-0a91742d179d
  Args:
    source: James_Coyle
    type: :Person
  AssignClass (127fe7f1-418a-45bd-b2fd-d2e7e0628c52)
 Call ID: 127fe7f1-418a-45bd-b2fd-d2e7e0628c52
  Args:
    source: Lady_Louise_Windsor
    type: :Woman
  AssignClass (d982194c-c36c-4668-91e0-8dc16b64c28b)
 Call ID: d982194c-c36c-4668-91e0-8dc16b64c28b
  Args:
    type: :Person
    source: Lady_Louise_Windsor
  AddLiteral (17312796-6736-4a13-a8ff-e3e1aab2d488)
 Call ID: 17312796-6736-4a13-a8ff-e3e1aab2d488
  Args:
    source: Lady_Louise_Windsor
    literal_type: xsd:integer
    literal_value: 2003
    relation: :hasBirthYear
  AssignClass (dceae698-2429-4dfa-9e31-fca8cd283d1d)
 Call ID: dceae698-2429-4dfa-9e31-fca8cd283d1d
  Args:
    source: Prince_Edward
    type: :Man
  AssignClass (aee328d0-15ee-422a-a011-b77110780d95)
 Call ID: aee328d0-15ee-422a-a011-b77110780d95
  Args:
    source: Prince_Edward
    type: :Person
  AssignClass (858c56cf-c56a-4e0e-8839-15c7f0ed3c3d)
 Call ID: 858c56cf-c56a-4e0e-8839-15c7f0ed3c3d
  Args:
    source: Sophie
    type: :Woman
  AssignClass (04dc07e2-1f17-4a97-854a-73891458eef5)
 Call ID: 04dc07e2-1f17-4a97-854a-73891458eef5
  Args:
    source: Sophie
    type: :Person
  AddTriple (aa22e611-edcb-4dcc-b3a6-9625c4b4bdc3)
 Call ID: aa22e611-edcb-4dcc-b3a6-9625c4b4bdc3
  Args:
    source: Lady_Louise_Windsor
    target: Prince_Edward
    relation: :hasFather
  AddTriple (8fd80540-3248-4310-93d5-eea5126b461d)
 Call ID: 8fd80540-3248-4310-93d5-eea5126b461d
  Args:
    source: Lady_Louise_Windsor
    target: Sophie
    relation: :hasMother
  Finish (3a597330-3de1-462a-9749-1458950932db)
 Call ID: 3a597330-3de1-462a-9749-1458950932db
  Args: