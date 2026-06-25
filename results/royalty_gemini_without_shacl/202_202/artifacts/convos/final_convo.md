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
Archduke Gottfried of Austria (German: Gottfried Maria Joseph Peter Ferdinand Hubert Anton Rupert Leopold Heinrich Ignaz Alfons, Erzherzog von Österreich, Prinz von Toskana; 14 March 1902 – 21 January 1984), also styled as Gottfried Erzherzog von Österreich, was an Archduke of Austria and claimant to the defunct throne of the Grand Duchy of Tuscany.
Biography

On 20 December 1866, Goffredo's grandfather, Ferdinando IV, the last Grand Duke of Tuscany, and his children were readmitted to the imperial family.
The House of Tuscany ceased to exist as a sovereign branch and merged with the Austrian imperial house.
Ferdinand was able to maintain his fons honorum vita natural durante, while his children became only imperial princes (archdukes of Austria) and no longer princes/princesses of Tuscany.
The Grand Magistry of the Order of St Stephen died out with the death of Ferdinand IV.
In fact, after the death of Grand Duke Ferdinand IV in 1908, Emperor Franz Joseph I forbade the acceptance of the title of Grand Duke or Prince or Princess of Tuscany: none of Ferdinand IV's children born after 1866 accepted the title of Prince or Grand Duke of Tuscany.
They were also unable to legitimately take possession of the extinct dynastic orders, previously conferred by the Grand Dukes of Tuscany.
While his grandfather had kept the title of Grand Duke of Tuscany after the abolition of the dukedom in 1860, he had abdicated it in favor of the Austrian Emperor in 1870.
Peter Ferdinand, Goffredo's father, never  claimed the title of Grand Duke of Tuscany.
The former Prime Minister of Saxony and later Imperial and Household Minister Beust declared: "The Tuscan Grand Ducal family has lost its sovereign rights as a result of political events.
The Grand Dukes Leopold and Ferdinand and their more famous brothers are therefore from now on to be considered only as Archdukes of Austria and to be treated in accordance with the Statute of the High Noble Family of 3 February 1839.
"


Family

Gottfried was born in Linz, Austria-Hungary, the eldest child and son  of Archduke Peter Ferdinand of Austria and his wife Princess Maria Cristina of Bourbon-Two Sicilies.
Gottfried was raised with his three siblings in Salzburg and Vienna until the end of World War I in 1918, when his family emigrated to Lucerne, Switzerland.
Marriage and issue

Gottfried married Princess Dorothea of Bavaria, fifth child and fourth daughter of Prince Franz of Bavaria and his wife Princess Isabella Antonie of Croÿ, on 2 August 1938 civilly and religiously on 3 August 1938 in Sárvár, Kingdom of Hungary.
Around 1970, in violation of the decree of Emperor Franz Joseph I of 1866 and ignoring the abdication of his grandfather last Grand Duke of Tuscany Ferdinand IV signed in Lindau on Lake Constance in 1870, he assumed the title of Grand Duke of Tuscany without the permission of the head of the imperial and royal house.
Gottfried and Dorothea had issue:


Honours

Ancestry

References



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
  AssignClass (7ab7b129-d973-4641-905e-0077ad95268f)
 Call ID: 7ab7b129-d973-4641-905e-0077ad95268f
  Args:
    source: :Gottfried
    type: :Man
  AssignClass (628010cb-2c4a-492a-948b-870c79b5cec3)
 Call ID: 628010cb-2c4a-492a-948b-870c79b5cec3
  Args:
    type: :Person
    source: :Gottfried
  AddLiteral (5a05d016-21da-4fc1-bff3-439d692dbc10)
 Call ID: 5a05d016-21da-4fc1-bff3-439d692dbc10
  Args:
    relation: :hasBirthYear
    literal_value: 1902
    source: :Gottfried
    literal_type: xsd:integer
  AddLiteral (ffc9f10c-755a-4de1-b2d0-0bccd47bd5db)
 Call ID: ffc9f10c-755a-4de1-b2d0-0bccd47bd5db
  Args:
    literal_value: 1984
    relation: :hasDeathYear
    source: :Gottfried
    literal_type: xsd:integer
  AssignClass (de4d2617-3502-479d-8180-dd094ff10842)
 Call ID: de4d2617-3502-479d-8180-dd094ff10842
  Args:
    source: :Ferdinando_IV
    type: :Man
  AssignClass (83a1ea43-bb19-4062-ba4e-658579b82d27)
 Call ID: 83a1ea43-bb19-4062-ba4e-658579b82d27
  Args:
    type: :Person
    source: :Ferdinando_IV
  AssignClass (8ac1c03e-a377-4771-9043-39b1ca8f007a)
 Call ID: 8ac1c03e-a377-4771-9043-39b1ca8f007a
  Args:
    type: :Man
    source: :Peter_Ferdinand
  AssignClass (45303aca-dda8-47e5-a58c-cde2e7ccb171)
 Call ID: 45303aca-dda8-47e5-a58c-cde2e7ccb171
  Args:
    type: :Person
    source: :Peter_Ferdinand
  AssignClass (c64576ca-df52-4ee5-a0ff-0b76d1496eed)
 Call ID: c64576ca-df52-4ee5-a0ff-0b76d1496eed
  Args:
    source: :Maria_Cristina
    type: :Woman
  AssignClass (9bc2825b-5118-4fba-b238-3dcdfc520e67)
 Call ID: 9bc2825b-5118-4fba-b238-3dcdfc520e67
  Args:
    type: :Person
    source: :Maria_Cristina
  AddTriple (804ac8cb-f0e5-4bbb-ac2a-f0e29d523fda)
 Call ID: 804ac8cb-f0e5-4bbb-ac2a-f0e29d523fda
  Args:
    source: :Gottfried
    target: :Peter_Ferdinand
    relation: :hasFather
  AddTriple (00704c30-1b8d-48ab-87d1-3b669e384047)
 Call ID: 00704c30-1b8d-48ab-87d1-3b669e384047
  Args:
    relation: :hasMother
    target: :Maria_Cristina
    source: :Gottfried
  AddTriple (1b0d914c-e333-4826-bd82-2169f92715df)
 Call ID: 1b0d914c-e333-4826-bd82-2169f92715df
  Args:
    target: :Ferdinando_IV
    relation: :hasFather
    source: :Peter_Ferdinand
  AssignClass (50913d47-6c66-4eda-b246-73d373458b81)
 Call ID: 50913d47-6c66-4eda-b246-73d373458b81
  Args:
    source: :Dorothea
    type: :Woman
  AssignClass (d881c6cd-8193-4727-95ce-5f45a747e2fd)
 Call ID: d881c6cd-8193-4727-95ce-5f45a747e2fd
  Args:
    source: :Dorothea
    type: :Person
  AssignClass (8dd8696d-a7e9-4bea-a666-fdb205e32d28)
 Call ID: 8dd8696d-a7e9-4bea-a666-fdb205e32d28
  Args:
    type: :Man
    source: :Franz_of_Bavaria
  AssignClass (72e758cd-97cc-490e-bfd5-64ae0b397951)
 Call ID: 72e758cd-97cc-490e-bfd5-64ae0b397951
  Args:
    type: :Person
    source: :Franz_of_Bavaria
  AssignClass (e386174a-0ff8-4021-92e3-a32f8a487343)
 Call ID: e386174a-0ff8-4021-92e3-a32f8a487343
  Args:
    source: :Isabella_Antonie
    type: :Woman
  AssignClass (0aef2ead-b7af-4be3-b833-aa48fbbf019d)
 Call ID: 0aef2ead-b7af-4be3-b833-aa48fbbf019d
  Args:
    type: :Person
    source: :Isabella_Antonie
  AddTriple (509e37d1-0e84-448a-bdbb-dcbe72795f77)
 Call ID: 509e37d1-0e84-448a-bdbb-dcbe72795f77
  Args:
    source: :Dorothea
    relation: :hasFather
    target: :Franz_of_Bavaria
  AddTriple (2c2a89c8-2545-4f74-8532-0d0322a2d360)
 Call ID: 2c2a89c8-2545-4f74-8532-0d0322a2d360
  Args:
    source: :Dorothea
    relation: :hasMother
    target: :Isabella_Antonie
  AddTriple (c89ad5e3-da40-4cdb-b714-38c8f8d2a80e)
 Call ID: c89ad5e3-da40-4cdb-b714-38c8f8d2a80e
  Args:
    source: :Gottfried
    relation: :hasRelation
    target: :Dorothea
  AddLiteral (8b369ba6-4b0d-454b-a5b3-e0abf1056f40)
 Call ID: 8b369ba6-4b0d-454b-a5b3-e0abf1056f40
  Args:
    literal_value: 1938
    relation: :hasMarriageYear
    source: :Gottfried
    literal_type: xsd:integer
  Finish (49540067-8546-4dd3-98a4-09e468db8c35)
 Call ID: 49540067-8546-4dd3-98a4-09e468db8c35
  Args: