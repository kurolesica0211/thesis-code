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
Princess Françoise d'Orléans (Françoise Isabelle Louise Marie; 25 December 1902 - 25 February 1953) was born an Orléans Princess of France and became a Princess of Greece and Denmark by marriage.
She was thus a member of the Greek royal family and a descendant of the "Citizen-King" Louis Philippe I.


Life

Françoise d'Orléans was born in Paris, the second daughter of Jean d'Orléans, duc de Guise (an Orléanist pretender to the throne of France under the name Jean III) and his wife, the French Princess Isabelle of Orléans.
Françoise's brother, Prince Henri, Count of Paris, succeeded their father as the Orleanist pretender, under the name Henri VI.
In Palermo on 11 February 1929, she married Prince Christopher of Greece and Denmark (1888–1940).
This was Christopher's second marriage - he was the youngest son of King George I of Greece (1845–1913) and his wife, Grand Duchess Olga Constantinovna of Russia (1851–1926).
Through his father, he was thus a grandson of King Christian IX of Denmark (1818–1906), nicknamed "the father-in-law of Europe" due to his six children all marrying into other royal families.
They had only one child, the writer Prince Michael of Greece and Denmark (1939–2024), whose marriage to the Greek artist Marina Karella (born 1940) did not conform to the laws of the royal house and thus deprived him of all right of succession to the Greek throne.
She is grandmother of Princess Alexandra of Greece, an artist, art collector, arts patron, and child life specialist.
Her other grand-daughter is Princess Olga of Greece, who married Prince Aimone of Savoy-Aosta, one of two claimants to be Head of the House of Savoy.
The civil war in Greece was preventing her from entering, and the British government refused to grant her asylum.
Françoise and her son Michael went to Paris, where they lived in the home of Princess Isabella and her second husband, Prince Pierre Murat.
Françoise did not want to see anyone in their residence and rarely left her rooms.
She is buried alongside her husband in Tatoi Royal Cemetery, Greece.



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
  AssignClass (b23c0d6c-c45b-4dc6-93ac-0a2651212837)
 Call ID: b23c0d6c-c45b-4dc6-93ac-0a2651212837
  Args:
    type: :Woman
    source: Françoise_d'Orléans
  AssignClass (9cb79942-bd2a-4961-ab14-f22b37a77c13)
 Call ID: 9cb79942-bd2a-4961-ab14-f22b37a77c13
  Args:
    type: :Person
    source: Françoise_d'Orléans
  AddLiteral (92b8eca0-f121-4d99-9432-b59cf05ddda8)
 Call ID: 92b8eca0-f121-4d99-9432-b59cf05ddda8
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Françoise_d'Orléans
    literal_value: 1902
  AddLiteral (8b4bf00d-c976-4d30-88c0-1efe61317bc8)
 Call ID: 8b4bf00d-c976-4d30-88c0-1efe61317bc8
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1953
    source: Françoise_d'Orléans
  AssignClass (4942b4fe-7dc3-4472-8de2-351eabfa82fb)
 Call ID: 4942b4fe-7dc3-4472-8de2-351eabfa82fb
  Args:
    source: Jean_d'Orléans
    type: :Man
  AssignClass (6b890a9c-f5e8-4b20-9045-3ec26be1113d)
 Call ID: 6b890a9c-f5e8-4b20-9045-3ec26be1113d
  Args:
    source: Jean_d'Orléans
    type: :Person
  AssignClass (893df712-e348-4bcc-a090-de8d77129862)
 Call ID: 893df712-e348-4bcc-a090-de8d77129862
  Args:
    source: Isabelle_of_Orléans
    type: :Woman
  AssignClass (0c489ce1-1646-45b9-89a3-5f17a345ac3f)
 Call ID: 0c489ce1-1646-45b9-89a3-5f17a345ac3f
  Args:
    type: :Person
    source: Isabelle_of_Orléans
  AddTriple (f1091101-9997-417d-bdf7-3acf6d099fde)
 Call ID: f1091101-9997-417d-bdf7-3acf6d099fde
  Args:
    source: Françoise_d'Orléans
    relation: :hasFather
    target: Jean_d'Orléans
  AddTriple (d02f0cdc-1137-41c2-b0b9-185738bf1a4f)
 Call ID: d02f0cdc-1137-41c2-b0b9-185738bf1a4f
  Args:
    relation: :hasMother
    target: Isabelle_of_Orléans
    source: Françoise_d'Orléans
  AssignClass (b0976c4a-5fbe-4f7a-9add-da20e7c701d4)
 Call ID: b0976c4a-5fbe-4f7a-9add-da20e7c701d4
  Args:
    source: Henri_Count_of_Paris
    type: :Man
  AssignClass (32b46459-fd6f-4fd6-99b9-3124953ca24f)
 Call ID: 32b46459-fd6f-4fd6-99b9-3124953ca24f
  Args:
    type: :Person
    source: Henri_Count_of_Paris
  AddTriple (d84dd5bf-6e1f-4db0-8ea8-12cedd31d893)
 Call ID: d84dd5bf-6e1f-4db0-8ea8-12cedd31d893
  Args:
    source: Françoise_d'Orléans
    relation: :isSiblingOf
    target: Henri_Count_of_Paris
  AddTriple (8065e746-eda6-4bc0-bb0b-16c6721a6733)
 Call ID: 8065e746-eda6-4bc0-bb0b-16c6721a6733
  Args:
    relation: :hasFather
    target: Jean_d'Orléans
    source: Henri_Count_of_Paris
  AssignClass (e21a1e1c-2cdc-45f5-b346-7ad38bab8eb5)
 Call ID: e21a1e1c-2cdc-45f5-b346-7ad38bab8eb5
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    type: :Man
  AssignClass (3a9c1150-9ad2-485c-9e6c-69d0cd8fd0e7)
 Call ID: 3a9c1150-9ad2-485c-9e6c-69d0cd8fd0e7
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    type: :Person
  AddLiteral (8547498b-0ec5-43f8-9f68-196f8662ceef)
 Call ID: 8547498b-0ec5-43f8-9f68-196f8662ceef
  Args:
    source: Françoise_d'Orléans
    literal_value: 1929
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (d6cfb342-8829-44d0-a4d6-0f1673b4d30f)
 Call ID: d6cfb342-8829-44d0-a4d6-0f1673b4d30f
  Args:
    source: Françoise_d'Orléans
    relation: :hasRelation
    target: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (1d3f04ae-ddb2-49f5-9851-51e472b06cc0)
 Call ID: 1d3f04ae-ddb2-49f5-9851-51e472b06cc0
  Args:
    source: King_George_I_of_Greece
    type: :Man
  AssignClass (574ef6f6-e636-4bfa-9a11-de28e7b509ed)
 Call ID: 574ef6f6-e636-4bfa-9a11-de28e7b509ed
  Args:
    type: :Person
    source: King_George_I_of_Greece
  AssignClass (25e29795-a5a9-415d-a156-fa3da5c9ea4f)
 Call ID: 25e29795-a5a9-415d-a156-fa3da5c9ea4f
  Args:
    source: Grand_Duchess_Olga_Constantinovna_of_Russia
    type: :Woman
  AssignClass (ffe5ffc1-1b25-4471-8ba7-a612c6434b09)
 Call ID: ffe5ffc1-1b25-4471-8ba7-a612c6434b09
  Args:
    source: Grand_Duchess_Olga_Constantinovna_of_Russia
    type: :Person
  AddTriple (6104499c-c5e9-46c6-8913-c7a5d50ee0df)
 Call ID: 6104499c-c5e9-46c6-8913-c7a5d50ee0df
  Args:
    relation: :hasFather
    target: King_George_I_of_Greece
    source: Prince_Christopher_of_Greece_and_Denmark
  AddTriple (39d77184-6f54-48ca-995e-05c64b0fecba)
 Call ID: 39d77184-6f54-48ca-995e-05c64b0fecba
  Args:
    relation: :hasMother
    target: Grand_Duchess_Olga_Constantinovna_of_Russia
    source: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (a420cff2-4cb1-4427-821c-e5a3af7510ee)
 Call ID: a420cff2-4cb1-4427-821c-e5a3af7510ee
  Args:
    type: :Man
    source: King_Christian_IX_of_Denmark
  AssignClass (03a53a9c-426c-4c48-8a7c-3c757c4e0f61)
 Call ID: 03a53a9c-426c-4c48-8a7c-3c757c4e0f61
  Args:
    type: :Person
    source: King_Christian_IX_of_Denmark
  AddTriple (e38d8f59-caa8-419e-8d41-856e3d5fbbf5)
 Call ID: e38d8f59-caa8-419e-8d41-856e3d5fbbf5
  Args:
    relation: :hasFather
    target: King_Christian_IX_of_Denmark
    source: King_George_I_of_Greece
  AssignClass (4db55b45-b363-42f8-a669-537eac8f2858)
 Call ID: 4db55b45-b363-42f8-a669-537eac8f2858
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    type: :Man
  AssignClass (02256ab4-6e50-48f1-9bcb-8b5535273578)
 Call ID: 02256ab4-6e50-48f1-9bcb-8b5535273578
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AddTriple (3d53f151-3dca-48e5-8a1d-acc8cf5eb5fe)
 Call ID: 3d53f151-3dca-48e5-8a1d-acc8cf5eb5fe
  Args:
    relation: :hasMother
    target: Françoise_d'Orléans
    source: Prince_Michael_of_Greece_and_Denmark
  AddTriple (2c4db222-1d63-410d-be1e-662dc722025b)
 Call ID: 2c4db222-1d63-410d-be1e-662dc722025b
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    relation: :hasFather
    target: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (dc708f21-e821-4730-9e58-f17e3c17c31b)
 Call ID: dc708f21-e821-4730-9e58-f17e3c17c31b
  Args:
    source: Marina_Karella
    type: :Woman
  AssignClass (2d195290-51ba-4480-ac9d-7eae4717b675)
 Call ID: 2d195290-51ba-4480-ac9d-7eae4717b675
  Args:
    source: Marina_Karella
    type: :Person
  AddTriple (739b07e8-29e5-4bd2-a937-27db48068bdc)
 Call ID: 739b07e8-29e5-4bd2-a937-27db48068bdc
  Args:
    relation: :hasRelation
    target: Marina_Karella
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (113d59ca-b476-45c6-9a0e-15071bf53401)
 Call ID: 113d59ca-b476-45c6-9a0e-15071bf53401
  Args:
    type: :Woman
    source: Princess_Alexandra_of_Greece
  AssignClass (fc0aa5d0-82a9-469d-9de7-7e2b25c57fbb)
 Call ID: fc0aa5d0-82a9-469d-9de7-7e2b25c57fbb
  Args:
    source: Princess_Alexandra_of_Greece
    type: :Person
  AssignClass (89624d72-c714-463a-bb64-fb254fe2d603)
 Call ID: 89624d72-c714-463a-bb64-fb254fe2d603
  Args:
    source: Princess_Olga_of_Greece
    type: :Woman
  AssignClass (5017f145-1732-4996-9ba2-735cb40c494e)
 Call ID: 5017f145-1732-4996-9ba2-735cb40c494e
  Args:
    type: :Person
    source: Princess_Olga_of_Greece
  AssignClass (2ca6c69a-f1b2-49b7-a2ab-e12dce0b060c)
 Call ID: 2ca6c69a-f1b2-49b7-a2ab-e12dce0b060c
  Args:
    source: Prince_Aimone_of_Savoy-Aosta
    type: :Man
  AssignClass (ef65452a-59e5-4ccf-a3ce-f995c7e460c6)
 Call ID: ef65452a-59e5-4ccf-a3ce-f995c7e460c6
  Args:
    type: :Person
    source: Prince_Aimone_of_Savoy-Aosta
  AddTriple (d3be4760-004b-4dfe-8ebe-74e572bc1462)
 Call ID: d3be4760-004b-4dfe-8ebe-74e572bc1462
  Args:
    source: Princess_Olga_of_Greece
    relation: :hasRelation
    target: Prince_Aimone_of_Savoy-Aosta
  AssignClass (2a38f8b5-78c6-474f-bec4-2d4fbab9dd49)
 Call ID: 2a38f8b5-78c6-474f-bec4-2d4fbab9dd49
  Args:
    type: :Woman
    source: Princess_Isabella_Murat
  AssignClass (20268954-4cc7-434f-aeb3-3e14d5e8cd23)
 Call ID: 20268954-4cc7-434f-aeb3-3e14d5e8cd23
  Args:
    type: :Person
    source: Princess_Isabella_Murat
  AssignClass (300ef745-e774-404f-9d2a-00484a420a21)
 Call ID: 300ef745-e774-404f-9d2a-00484a420a21
  Args:
    source: Prince_Pierre_Murat
    type: :Man
  AssignClass (19b20e94-421b-45d4-a085-7ea5d79c3698)
 Call ID: 19b20e94-421b-45d4-a085-7ea5d79c3698
  Args:
    source: Prince_Pierre_Murat
    type: :Person
  AddTriple (a785a19e-6700-4ec7-9efe-d083a4ecd3ac)
 Call ID: a785a19e-6700-4ec7-9efe-d083a4ecd3ac
  Args:
    relation: :hasRelation
    target: Prince_Pierre_Murat
    source: Princess_Isabella_Murat
  Finish (128993b1-0e9c-4cd8-9130-544ff7689a42)
 Call ID: 128993b1-0e9c-4cd8-9130-544ff7689a42
  Args: