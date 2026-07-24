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
Countess Walburga Douglas (née von Habsburg-Lothringen; born 5 October 1958) is a German-born Swedish lawyer and politician, who served as a member of the Riksdag of Sweden for the Moderate Party from 2006 to 2014.
Early life

Born in 1958 in Berg am Starnberger See, West Germany, she is the fifth daughter of Otto von Habsburg, the last crown prince of Austria-Hungary, and his wife Princess Regina of Saxe-Meiningen.
Walburga was banished from the Republic of Austria from birth and well into adult life, along with her siblings, by the Habsburg Law that had been in effect since 1938, having been (re)imposed by the Nazis.
She is a granddaughter of the last Austrian emperor, Charles I, and a member of the House of Habsburg-Lorraine.
Her ancestral titles (abolished in Austria since 1919) are Archduchess Walburga of Austria, Archduchess of Austria, Princess of Hungary and Bohemia, with the style of Her Imperial and Royal Highness (HI&RH).
She does not currently use her ancestral titles actively in her daily life; however, by law she holds the title of Countess Douglas in the Kingdom of Sweden, her current country of residence and citizenship.
On 17 September 2023, Douglas visited Armenia to dedicate the opening of the PanEuropa Armenia branch in Yerevan.
Personal life

On 5 December 1992 in Budapest, Hungary, Walburga married a Swedish nobleman, Count Carl Axel Archibald Douglas (born 27 November 1949 in Stockholm), son of Count Archibald Douglas and Baroness Margareta Lagerfelt.
Her husband's family is a  noble family in Sweden, descended from the Scot Robert Douglas, Count of Skenninge, member of the Scottish Clan Douglas and founder of its Swedish branch.
Her husband is a first cousin of Count Gustaf Douglas and his sisters Rosita Spencer-Churchill, Duchess of Marlborough, and Princess Elisabeth, Duchess in Bavaria, the wife of Prince Max, Duke in Bavaria.
They have a son, Count Mauritz Otto Wenzel Douglas (born 30 March 1994 in Stockholm).



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
  AssignClass (209eff58-5d20-499b-9daa-2460550fe7ca)
 Call ID: 209eff58-5d20-499b-9daa-2460550fe7ca
  Args:
    type: :Woman
    source: :WalburgaDouglas
  AssignClass (c21c4d09-8930-4e5f-823f-349b073c5b51)
 Call ID: c21c4d09-8930-4e5f-823f-349b073c5b51
  Args:
    type: :Person
    source: :WalburgaDouglas
  AddLiteral (e0ab8e4e-61de-4d48-91e0-7e94abed7aaa)
 Call ID: e0ab8e4e-61de-4d48-91e0-7e94abed7aaa
  Args:
    literal_type: xsd:integer
    source: :WalburgaDouglas
    relation: :hasBirthYear
    literal_value: 1958
  AssignClass (d0df8059-832c-45d9-9ef7-fd3df94e45ce)
 Call ID: d0df8059-832c-45d9-9ef7-fd3df94e45ce
  Args:
    source: :OttoVonHabsburg
    type: :Man
  AssignClass (e69030f7-b58e-49af-aad0-123479fab0bd)
 Call ID: e69030f7-b58e-49af-aad0-123479fab0bd
  Args:
    source: :OttoVonHabsburg
    type: :Person
  AssignClass (fa0a00f6-9e46-4ae1-9fce-bd7c087dce51)
 Call ID: fa0a00f6-9e46-4ae1-9fce-bd7c087dce51
  Args:
    source: :OttoVonHabsburg
    type: :Ancestor
  AssignClass (b3f8aedf-4090-4c82-b995-e4f2a9f96e74)
 Call ID: b3f8aedf-4090-4c82-b995-e4f2a9f96e74
  Args:
    type: :Woman
    source: :ReginaOfSaxeMeiningen
  AssignClass (10409137-2076-4295-95bc-824bb63c677c)
 Call ID: 10409137-2076-4295-95bc-824bb63c677c
  Args:
    type: :Person
    source: :ReginaOfSaxeMeiningen
  AssignClass (bbc05544-9438-4d60-9263-f293dd651fa0)
 Call ID: bbc05544-9438-4d60-9263-f293dd651fa0
  Args:
    type: :Ancestor
    source: :ReginaOfSaxeMeiningen
  AddTriple (14f91255-e7b0-41ae-866b-4cd267dbe02a)
 Call ID: 14f91255-e7b0-41ae-866b-4cd267dbe02a
  Args:
    target: :OttoVonHabsburg
    source: :WalburgaDouglas
    relation: :hasFather
  AddTriple (c041f37c-7b3b-449a-896c-44c1677d7a1b)
 Call ID: c041f37c-7b3b-449a-896c-44c1677d7a1b
  Args:
    source: :WalburgaDouglas
    relation: :hasMother
    target: :ReginaOfSaxeMeiningen
  AssignClass (90c8c89e-39c9-4624-981b-92c24e42f68e)
 Call ID: 90c8c89e-39c9-4624-981b-92c24e42f68e
  Args:
    source: :CarlAxelArchibaldDouglas
    type: :Man
  AssignClass (f36b2f09-e60f-4108-99d5-3106150785b2)
 Call ID: f36b2f09-e60f-4108-99d5-3106150785b2
  Args:
    source: :CarlAxelArchibaldDouglas
    type: :Person
  AddLiteral (3575e8fc-d8fc-47a3-a629-57bcc950c560)
 Call ID: 3575e8fc-d8fc-47a3-a629-57bcc950c560
  Args:
    literal_value: 1949
    literal_type: xsd:integer
    source: :CarlAxelArchibaldDouglas
    relation: :hasBirthYear
  AddLiteral (dc0340d6-d0ed-4b4e-bebf-37d21481cb46)
 Call ID: dc0340d6-d0ed-4b4e-bebf-37d21481cb46
  Args:
    relation: :hasMarriageYear
    source: :WalburgaDouglas
    literal_type: xsd:integer
    literal_value: 1992
  AddTriple (83f4ce1f-eb3f-43d4-9b35-3005efc6f895)
 Call ID: 83f4ce1f-eb3f-43d4-9b35-3005efc6f895
  Args:
    target: :CarlAxelArchibaldDouglas
    source: :WalburgaDouglas
    relation: :hasRelation
  AssignClass (19993845-2a67-4729-835a-71dc2d315342)
 Call ID: 19993845-2a67-4729-835a-71dc2d315342
  Args:
    type: :Man
    source: :ArchibaldDouglas
  AssignClass (7b055d7f-0cad-43d7-a070-aec1aad55cff)
 Call ID: 7b055d7f-0cad-43d7-a070-aec1aad55cff
  Args:
    source: :ArchibaldDouglas
    type: :Person
  AssignClass (deabc8d8-b1c1-4fd8-990b-b04c62c128a4)
 Call ID: deabc8d8-b1c1-4fd8-990b-b04c62c128a4
  Args:
    source: :MargaretaLagerfelt
    type: :Woman
  AssignClass (cf18db33-fa25-4103-bcf0-4809e608e6be)
 Call ID: cf18db33-fa25-4103-bcf0-4809e608e6be
  Args:
    type: :Person
    source: :MargaretaLagerfelt
  AddTriple (da330944-8520-402c-b052-6ec747011d1c)
 Call ID: da330944-8520-402c-b052-6ec747011d1c
  Args:
    target: :ArchibaldDouglas
    source: :CarlAxelArchibaldDouglas
    relation: :hasFather
  AddTriple (f6024e8a-4b85-41cf-a507-212b75b4fff5)
 Call ID: f6024e8a-4b85-41cf-a507-212b75b4fff5
  Args:
    target: :MargaretaLagerfelt
    relation: :hasMother
    source: :CarlAxelArchibaldDouglas
  AssignClass (2ba07896-f36e-489e-9f4b-bbd540bbd640)
 Call ID: 2ba07896-f36e-489e-9f4b-bbd540bbd640
  Args:
    type: :Man
    source: :MauritzOttoWenzelDouglas
  AssignClass (39d9b0a8-2959-4b2c-83c9-11770c166bba)
 Call ID: 39d9b0a8-2959-4b2c-83c9-11770c166bba
  Args:
    type: :Person
    source: :MauritzOttoWenzelDouglas
  AddLiteral (f9955e4c-a709-45ec-9922-1b4f79ec0042)
 Call ID: f9955e4c-a709-45ec-9922-1b4f79ec0042
  Args:
    relation: :hasBirthYear
    source: :MauritzOttoWenzelDouglas
    literal_type: xsd:integer
    literal_value: 1994
  AddTriple (cfe9fd46-ef3c-4a39-b008-b7dd9898aa21)
 Call ID: cfe9fd46-ef3c-4a39-b008-b7dd9898aa21
  Args:
    source: :MauritzOttoWenzelDouglas
    relation: :hasFather
    target: :CarlAxelArchibaldDouglas
  AddTriple (5d3bf803-74c4-4b7c-a0a3-e7e949279622)
 Call ID: 5d3bf803-74c4-4b7c-a0a3-e7e949279622
  Args:
    source: :MauritzOttoWenzelDouglas
    relation: :hasMother
    target: :WalburgaDouglas
  AssignClass (f6b9d7bd-9015-44cd-8732-fb144b105489)
 Call ID: f6b9d7bd-9015-44cd-8732-fb144b105489
  Args:
    source: :CharlesI
    type: :Man
  AssignClass (0275977e-1944-473b-b481-c31c2e8da8f4)
 Call ID: 0275977e-1944-473b-b481-c31c2e8da8f4
  Args:
    source: :CharlesI
    type: :Person
  AssignClass (2fdc3d9d-1473-4361-b8fa-4288b22200f6)
 Call ID: 2fdc3d9d-1473-4361-b8fa-4288b22200f6
  Args:
    type: :Ancestor
    source: :CharlesI
  AddTriple (2dca086b-35f0-4e59-b5d6-fcbebba6aa25)
 Call ID: 2dca086b-35f0-4e59-b5d6-fcbebba6aa25
  Args:
    relation: :hasAncestor
    source: :WalburgaDouglas
    target: :CharlesI
  Finish (11306647-340a-4185-8d5d-9bd0c5b31c80)
 Call ID: 11306647-340a-4185-8d5d-9bd0c5b31c80
  Args: